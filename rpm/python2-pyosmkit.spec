%global srcname pyosmkit
%global gitname pyosm

Name:           python-%{srcname}
Version:        0.11
Release:        1%{?dist}
Summary:        Example python module

License:        MIT
URL:            https://github.com/tierpod/pyosm
Source0:        https://github.com/tierpod/pyosm/archive/v%{version}.tar.gz

BuildArch:      noarch

%description
Library for building OSM tools.

%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python2-devel
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
Library for building OSM tools.

%prep
%autosetup -n %{gitname}-%{version}

%build
%py2_build

%install
%py2_install

# Note that there is no %%files section for the unversioned python module
%files -n python2-%{srcname}
%license LICENSE
%doc README.md
%{python2_sitelib}/%{srcname}-*.egg-info/
%{python2_sitelib}/%{srcname}/
%{_bindir}/osmtool_*
