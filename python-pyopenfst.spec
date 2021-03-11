#
# Conditional build:
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define		rel	3

Summary:	PyOpenFST - Python 2 bindings to OpenFTS library
Summary(pl.UTF-8):	PyOpenFST - wiązania Pythona 2 do biblioteki OpenFST
Name:		python-pyopenfst
Version:	0.4
%define	snap	20141029
%define	gitref	eb0c0f9af57bb597f9511e1cc69cbbefe50ff507
Release:	0.%{snap}.%{rel}
License:	Apache v2.0
Group:		Libraries/Python
Source0:	https://github.com/tmbdev/pyopenfst/archive/%{gitref}/pyopenfst-%{snap}.tar.gz
# Source0-md5:	39e3516a6d80cd2604d9dc76de48a9a5
Patch0:		pyopenfst-update.patch
Patch1:		pyopenfst-tests.patch
Patch2:		pyopenfst-python3.patch
URL:		https://github.com/tmbdev/pyopenfst
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	openfst-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	swig-python >= 2
%if %{with python2}
BuildRequires:	python-devel >= 2.0
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
%endif
Requires:	python-libs >= 2.0
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The OpenFST library implements algorithms on weighted finite state
transducers. The PyOpenFST project contains bindings for the library.

%description -l pl.UTF-8
Biblioteka OpenFST implementuje algorytmy na automatach skończonych z
wyjściem i wagami. Projekt PyOpenFST zawiera wiązania Pythona do
biblioteki.

%package -n python3-pyopenfst
Summary:	PyOpenFST - Python 3 bindings to OpenFTS library
Summary(pl.UTF-8):	PyOpenFST - wiązania Pythona 3 do biblioteki OpenFST
Group:		Libraries/Python
Requires:	python3-libs >= 1:3.2

%description -n python3-pyopenfst
The OpenFST library implements algorithms on weighted finite state
transducers. The PyOpenFST project contains bindings for the library.

%description -n python3-pyopenfst -l pl.UTF-8
Biblioteka OpenFST implementuje algorytmy na automatach skończonych z
wyjściem i wagami. Projekt PyOpenFST zawiera wiązania Pythona do
biblioteki.

%prep
%setup -q -n pyopenfst-%{gitref}
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
# setup.py uses CFLAGS for C++; openfst requires C++11
CFLAGS="%{rpmcxxflags} -std=c++11"

%if %{with python2}
%py_build

%if %{with tests}
PYTHONPATH=$(echo build-2/lib.*) \
%{__python} -munittest test-openfst test-openfst0 test-openfst1
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
PYTHONPATH=$(echo build-3/lib.*) \
%{__python3} -munittest test-*.py
%endif
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install
%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python-pyopenfst-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python-pyopenfst-%{version}
%{__sed} -E -i -e '1s,#!\s*/usr/bin/python(\s|$),#!%{__python}\1,' \
	$RPM_BUILD_ROOT%{_examplesdir}/python-pyopenfst-%{version}/*
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-pyopenfst-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-pyopenfst-%{version}
%{__sed} -E -i -e '1s,#!\s*/usr/bin/python(\s|$),#!%{__python3}\1,' \
	$RPM_BUILD_ROOT%{_examplesdir}/python3-pyopenfst-%{version}/*
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc README.md
%{py_sitedir}/openfst.py[co]
%attr(755,root,root) %{py_sitedir}/_openfst.so
%{py_sitedir}/openfst-%{version}-py*.egg-info
%dir %{_examplesdir}/%{name}-%{version}
%attr(755,root,root) %{_examplesdir}/%{name}-%{version}/dict2linefst
%attr(755,root,root) %{_examplesdir}/%{name}-%{version}/lines2linefst
%attr(755,root,root) %{_examplesdir}/%{name}-%{version}/pyfst-*
%attr(755,root,root) %{_examplesdir}/%{name}-%{version}/test-ngraph
%attr(755,root,root) %{_examplesdir}/%{name}-%{version}/text2ngraphfst
%attr(755,root,root) %{_examplesdir}/%{name}-%{version}/wdict2wordfst
%{_examplesdir}/%{name}-%{version}/dict-*
%endif

%if %{with python3}
%files -n python3-pyopenfst
%defattr(644,root,root,755)
%doc README.md
%{py3_sitedir}/openfst.py
%attr(755,root,root) %{py3_sitedir}/_openfst.cpython-*.so
%{py3_sitedir}/__pycache__/openfst.cpython-*.py[co]
%{py3_sitedir}/openfst-%{version}-py*.egg-info
%dir %{_examplesdir}/python3-pyopenfst-%{version}
%attr(755,root,root) %{_examplesdir}/python3-pyopenfst-%{version}/dict2linefst
%attr(755,root,root) %{_examplesdir}/python3-pyopenfst-%{version}/lines2linefst
%attr(755,root,root) %{_examplesdir}/python3-pyopenfst-%{version}/pyfst-*
%attr(755,root,root) %{_examplesdir}/python3-pyopenfst-%{version}/test-ngraph
%attr(755,root,root) %{_examplesdir}/python3-pyopenfst-%{version}/text2ngraphfst
%attr(755,root,root) %{_examplesdir}/python3-pyopenfst-%{version}/wdict2wordfst
%{_examplesdir}/python3-pyopenfst-%{version}/dict-*
%endif
