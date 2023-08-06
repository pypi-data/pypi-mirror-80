#!/usr/bin/env python
#

import os, hashlib
import sys
import requests
import warnings
import numpy as np
LOGIN_URL = "https://irsa.ipac.caltech.edu/account/signon/login.do"

import base64
if sys.version_info > (3,0):
    from configparser import ConfigParser
    _PYTHON3 = True
else:
    from ConfigParser import ConfigParser
    _PYTHON3 = False
    
_SOURCEDIR = os.path.dirname(os.path.realpath(__file__))


_ENCRYPT_FILE = os.path.expanduser("~")+"/.ztfquery"
_ENCRYPTING_FILE = os.path.expanduser("~")+"/.queryirsa"


LOCALSOURCE   = os.getenv('ZTFDATA',"./Data/")


# ================= #
#  Crypting         #
# ================= #

def _load_id_(which, askit=True):
    """ returns login information for the requested enty"""
    import base64
    config = ConfigParser()
    config.read( _ENCRYPT_FILE )
    if which not in config.sections():
        if not askit:
            raise AttributeError(f"No {which} account setup. Add then in .ztfquery or run ztfquery.io.set_account({which})"%(which,which))
        else:
            warnings.warn(f"No {which} account setup, please provide it")
            set_account(which)
            config = ConfigParser()
            config.read( _ENCRYPT_FILE )

    if _PYTHON3:
        return config[which.lower()]["username"], base64.b64decode(config[which.lower()]["password"][2:-1]).decode("utf-8")
    else:
        return config.get(which.lower(),"username"), base64.b64decode(config.get(which.lower(),"password"))

def set_account(which, username=None, password=None, test=True, force=False):
    """ Setup the username and password (simply encrypted!) for the given `which` account. 
    Saved in ~/.ztfquery
    """
    import base64
    import getpass
    config = ConfigParser()
    config.read( _ENCRYPT_FILE )
    # - Name & Password
    if username is None:
        if _PYTHON3:
            username = input('Enter your %s login: '%which)
        else:
            username = raw_input('Enter your %s login: '%which)
            
    if password is None:
        password = getpass.getpass()
        
    # - Check inputs
    if test:
        wrong_ = False
        if which == "irsa":
            if not test_irsa_account([username, password]):
                warnings.warn("The irsa_test for you account returns False. Most likely you provided incorrect logins")
                wrong_ = True
        else:
            warnings.warn("No test designed for %s. Cannot test if logins are correct."%which)
        if wrong_ and not force:
            raise ValueError("Bad username/passworg for %s. force=False so the logins are not stored. "%which)
            
    password_ = base64.b64encode( password.encode("utf-8") )
    if _PYTHON3:
        config[which.lower()] = {"username":username, "password": password_ }        
    else:
        section = which.lower()
        if section not in config.sections():
            config.add_section(section)
        config.set(section,"username",username)
        config.set(section,"password",password_)

        
    with open( _ENCRYPT_FILE , 'w') as configfile:
        config.write(configfile)
        

#
# TEST
#
# - Password testing
def test_irsa_account(auth=None):
    """  returns True if the IRSA account is correctly set. """
    if auth is None:
        auth = _load_id_("irsa")
    return ".ipac.caltech.edu" in get_cookie(*auth)._cookies



# - File testing
def get_localfiles(extension="*", startpath=None):
    """ Look for all file with the given extension recursively starting from `startpath`.
    (based on glob)
    
    Parameters
    ----------
    extension: [string] -optional-
        All the 'file.{}'.format(extension) will be looked at.
        (first '.' ignored such that extension='.fits' is equivalent to extension='fits')

    startpath: [None or path] -optional-
        From which directory does this start to look at.
        If None: $ZTFDATA (stored as io.LOCALSOURCE) will be used.

    Returns
    -------
    list of file.
    """
    from glob import glob
    if startpath is None:
        startpath = LOCALSOURCE
    if extension.startswith("."):
        extension = extension[1:]
        
    return [f for f in glob(startpath + "**/*.%s"%extension, recursive=True)]

def run_full_filecheck(extension="*", startpath=None,
                        erasebad=True, redownload=False, 
                        nprocess=4, show_progress=True, notebook=False,
                        **kwargs ):
    """ Look for all file with the given extension recursively starting from `startpath` and checks if the file 
    is usable ok not. This returns the bad files.
    
    Parameters
    ----------

    // Data files
    extension: [string] -optional-
        All the 'file.{}'.format(extension) will be looked at.
        (first '.' ignored such that extension='.fits' is equivalent to extension='fits')

    startpath: [None or path] -optional-
        From which directory does this start to look at.
        If None: $ZTFDATA (stored as io.LOCALSOURCE) will be used.

    // Check options

    erasebad: [bool] -optional-
        Do you want to remove from your local directory the corrupted files ?
        
    redownload: [bool] -optional-
        Shall corrupted file be automatically re downloaded ?
        (Only works for IRSA files ('/sci/','/raw/', '/ref/', '/cal/')

    nprocess: [int] -optional-
        Number of paralell processing

    show_progress: [bool] -optional-
        Do you want to show the progress bar ?
        
    notebook: [bool]
        Are you running from a notebook. 
        Ignored if show_progress=False

    Returns
    -------
    list of corrupted/bad files (might already be removed, see erasebad)

    """
    all_ztffiles = get_localfiles(extension=extension, startpath=startpath)
    print("%d files to check"%len(all_ztffiles))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        badfiles = test_files(all_ztffiles, erasebad=erasebad, nprocess=nprocess,
                             show_progress=show_progress, notebook=notebook,
                             redownload=redownload, **kwargs)
        
    return badfiles
    
def test_files(filename, erasebad=True, nprocess=1, show_progress=True, notebook=False,
                   redownload=False, **kwargs ):
    """ 
    
    Parameters
    ----------
    filename: [fiulepath or list of]
        File(s) to be checked. 

    erasebad: [bool] -optional-
        Do you want to remove from your local directory the corrupted files ?
        
    redownload: [bool] -optional-
        Shall corrupted file be automatically re downloaded ?
        (Only works for IRSA files ('/sci/','/raw/', '/ref/', '/cal/')

    nprocess: [int] -optional-
        Number of paralell processing

    show_progress: [bool] -optional-
        Do you want to show the progress bar ?
        
    notebook: [bool]
        Are you running from a notebook. 
        Ignored if show_progress=False
       
    Returns
    -------
    list of corrupted/bad files (might already be removed, see erasebad)

    """
    if nprocess is None:
        nprocess = 1
    elif nprocess<1:
        raise ValueError("nprocess must 1 or higher (None means 1)")

    filename = np.atleast_1d(filename)
    
    if nprocess == 1:
        fileissue = [f for f in filename if not _test_file_(f, erasebad=erasebad,
                                                            redownload=redownload,
                                                            **kwargs)]
    else:
        import multiprocessing
        if show_progress:
            from astropy.utils.console import ProgressBar
            bar = ProgressBar( len(filename), ipython_widget=notebook)
        else:
            bar = None

        erasebad_   = [erasebad]*len(filename)
        fileissue = []
        
        with multiprocessing.Pool(nprocess) as p:
            # Da Loop
            for j, isgood in enumerate( p.imap(_test_file_multiprocess_, zip(filename, erasebad_)) ):
                if bar is not None:
                    bar.update(j)
                if not isgood:
                    fileissue.append(filename[j])
                    
            if bar is not None:
                bar.update( len(filename) )
                
    if len(fileissue) >0:
        warnings.warn("%d file failed"%len(fileissue))
        if redownload:
            from .buildurl import _localsource_to_source_
            to_download_urls, locations = np.asarray([_localsource_to_source_(filename)
                                                        for filename in fileissue]).T
            source_to_dl = ["irsa"]
            for source in source_to_dl:
                source_dl = np.in1d(locations, [source])
                print("Downloading %d files from %s"%(len(source_dl[source_dl]), source))
                download_url(np.asarray(to_download_urls)[source_dl], np.asarray(fileissue)[source_dl],
                                 show_progress=show_progress, notebook=notebook, verbose=True,
                                 overwrite=True, nprocess=nprocess, cookies=get_cookie(*_load_id_(source)),
                         **kwargs)
            for source_ in np.unique(locations):
                if source_ is not None and source_ not in source_to_dl:
                    warnings.warn("files from %s have not downloaded (not implemented)."%source_)
                
        return fileissue
        

def _test_file_multiprocess_(args):
    """ """
    filename, erasebad = args
    return _test_file_(filename, erasebad=erasebad, fromdl=False, redownload=False)

def _test_file_(filename, erasebad=True, fromdl=False,
                redownload=False, verbose=True):
    """ """
    propissue = dict(erasebad=erasebad, fromdl=fromdl, redownload=redownload, verbose=verbose)
    # Fits file
    if ".fits" in filename:
        from astropy.io import fits
        if not hash_for_file_exists(filename):
            try:
                _ = fits.getdata(filename)
                calculate_and_write_hash(filename)
            except FileNotFoundError:
                warnings.warn("[Errno 2] No such file or directory: %s"%filename)
            except:
                _fileissue_(filename, **propissue)
                return False
        
    # txt file        
    elif ".txt" in filename:
        if not hash_for_file_exists(filename):
            try:
                _ = open(filename).read().splitlines()
                calculate_and_write_hash(filename)
            except FileNotFoundError:
                warnings.warn("[Errno 2] No such file or directory: %s"%filename)
            except:
                _fileissue_(filename, **propissue)
                return False
        
    # other extensions        
    else:
        warnings.warn("no file testing made for .%s files"%filename.split(".")[-1])
            
    return True

def _fileissue_(filename, erasebad=True, fromdl=False, redownload=False, verbose=True):
    """ """
    if fromdl:
        warnings.warn("Download failed %s seems corrupted (cannot open)"%filename)
    else:
        warnings.warn("cannot open file %s"%filename)
        
    if erasebad:
        warnings.warn("removing %s")
        os.remove(filename)
    else:
        warnings.warn("%s NOT ERASED")

    if redownload:
        from .buildurl import _localsource_to_source_
        url_to_dl, location = _localsource_to_source_(filename)
        if url_to_dl is not None:
            download_single_url(url_to_dl, fileout=filename, overwrite=True, verbose=verbose,
                                cookies = get_cookie(*_load_id_(location))
                                )
        else:
            warnings.warn("No url to donwload, redownload ignored")
    
# ================= #
#   Logging Tools   #
# ================= #
def get_cookie(username, password):
    """Get a cookie from the IPAC login service

    Parameters
    ----------
    username: [str]
        The IPAC account username
    password: [str]
        The IPAC account password
    """
    url = "%s?josso_cmd=login&josso_username=%s&josso_password=%s" % (LOGIN_URL, username, password)
    return requests.get(url).cookies


def _download_(args):
    """ To be used within _ZTFDownloader_.download_data() 
    url, fileout,overwrite,verbose = args
    """
    url, fileout,  overwrite, verbose = args
    download_single_url(url, fileout=fileout, overwrite=overwrite, verbose=verbose)


def download_from_filename(filename, suffix=None, verbose=False, overwrite=False,
                               auth=None, **kwargs):
    """ Download the file associated to the given filename """
    from .buildurl import filename_to_scienceurl
    if auth is None:
        auth = _load_id_("irsa")
    cookies = get_cookie(*auth)
        
    irsa_filename = filename_to_scienceurl(filename, suffix=suffix, verbose=verbose, source="irsa")
    local_filename = filename_to_scienceurl(filename, suffix=suffix, verbose=verbose, source="local")
    
    download_url(np.atleast_1d(irsa_filename),
                 np.atleast_1d(local_filename),
                 overwrite=overwrite,
                 cookies = cookies, **kwargs)
    
    
    
def download_url(to_download_urls, download_location,
                show_progress = True, notebook=False, verbose=True,
                overwrite=False, nprocess=None, cookies=None,
                **kwargs):
    """ """
    if nprocess is None:
        nprocess = 1
    elif nprocess<1:
        raise ValueError("nprocess must 1 or higher (None means 1)")

    if nprocess == 1:
        # Single processing
        if verbose:
            warnings.warn("No parallel downloading")
        for url, fileout in zip(to_download_urls, download_location):
            download_single_url(url,fileout=fileout, show_progress=show_progress,
                                    notebook=notebook, 
                                    overwrite=overwrite, verbose=verbose, cookies=cookies, **kwargs)
    else:
        # Multi processing
        import multiprocessing
        if show_progress:
            from astropy.utils.console import ProgressBar
            bar = ProgressBar( len(to_download_urls), ipython_widget=notebook)
        else:
            bar = None
                
        if verbose:
            warnings.warn("parallel downloading ; asking for %d processes"%nprocess)

        # Passing arguments
        overwrite_ = [overwrite]*len(to_download_urls)
        verbose_   = [verbose]*len(to_download_urls)
        with multiprocessing.Pool(nprocess) as p:
            # Da Loop
            for j, result in enumerate( p.imap_unordered(_download_, zip(to_download_urls,
                                                                    download_location,
                                                                 overwrite_, verbose_))):
                if bar is not None:
                    bar.update(j)
                    
            if bar is not None:
                bar.update( len(to_download_urls) )

            
def download_single_url(url, fileout=None, 
                        overwrite=False, verbose=True, cookies=None,
                        show_progress=True, notebook=False, chunk=1024,
                        filecheck=True, erasebad=True,
                        **kwargs):
    """ Download the url target using requests.get.
    the data is returned (if fileout is None) or stored in `fileout`
    Pa
    """
    if fileout is not None and not overwrite and os.path.isfile( fileout ):
        if verbose:
            warnings.warn("%s already exists: skipped"%fileout)
        return
    else:
        if verbose and fileout:
            warnings.warn("downloading %s to %s"%(url,fileout))

    # = Password and Username
    if cookies is None:
        cookies = get_cookie(*_load_id_("irsa"))

    # - requests options 
    download_prop = dict(cookies=cookies, stream=True)
    for k,v in kwargs.items():
        download_prop[k] = v
        
    if cookies in ["no_cookies"]:
        _ = download_prop.pop("cookies")

    request_fnc = "get" if not "data" in download_prop else "post"
    # = Where should the data be saved?
    if fileout is not None:
        directory = os.path.dirname(fileout)
        if not os.path.exists(directory):
            os.makedirs(directory)

    else:
        download_prop["stream"] = False
        return getattr(requests,request_fnc)(url, **download_prop)

    # With Progress bar?
    if not show_progress:
        response = getattr(requests,request_fnc)(url, **download_prop)
        if response.status_code == 200:
            with open(fileout, 'wb') as f:
                for data in response.iter_content(chunk):
                    f.write(data)
    
    else:
        from astropy.utils.console import ProgressBar
        response = getattr(requests,request_fnc)(url, **download_prop)
        if response.status_code == 200:
            chunk_barstep = 500
            f = open(fileout, 'wb')
            with ProgressBar(int(response.headers.get('content-length'))/(chunk_barstep*chunk),
                             ipython_widget=notebook) as bar:
                for i,data in enumerate(response.iter_content(chunk_size=chunk)):
                    if i%chunk_barstep==0:
                        bar.update()
                    f.write(data)
            f.close()
            calculate_and_write_hash(fileout)

    if filecheck:
        _test_file_(fileout, erasebad=erasebad, fromdl=True)

def calculate_hash(fname):
    """ """
    f = open(fname, 'rb')
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: f.read(4096), b""):
        hash_md5.update(chunk)
    hexdigest = hash_md5.hexdigest()
    f.close()
    return hexdigest

def calculate_and_write_hash(fname):
    """ """
    f = open(fname, 'rb')
    hash_md5 = hashlib.md5()
    for chunk in iter(lambda: f.read(4096), b""):
        hash_md5.update(chunk)
    hexdigest = hash_md5.hexdigest()
    f.close()
    f_hash = open(f"{fname}.md5", 'w')
    f_hash.write(hexdigest)
    f_hash.close()

def read_hash(fname):
    """ """
    f_hash = open(f"{fname}.md5", 'r')
    hash_md5 = f_hash.read()
    return hash_md5

def compare_hash(fname):
    """ """
    f_hash = open(hash_fname, 'r')
    hash_md5_read = f_hash.read()
    hash_md5_calculated = calculate_hash(fname)
    if hash_md5_read == hash_md5_calculated:
        return True
    else:
        return False

def hash_for_file_exists(fname):
    """ """
    return os.path.exists(f"{fname}.md5")
