%global srcname pyosmkit
%global gitname pyosm

Name:           python-%{srcname}
Version:        0.12
Release:        1%{?dist}
Summary:        Example python module

License:        MIT
URL:            https://github.com/tierpod/pyosm
Source0:        https://github.com/tierpod/pyosm/archive/v%{version}.tar.gz

BuildArch:      noarch

%description
Library for building OSM tools.

%package -n python3-%{srcname}
Summary:        Library for building OSM tools
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%{?python_provide:%python_provide python3-%{srcname}}

%description -n python3-%{srcname}
Library for building OSM tools.

%prep
%autosetup -n %{gitname}-%{version}

%build
%py3_build

%install
%py3_install

# Note that there is no %%files section for the unversioned python module
%files -n python3-%{srcname}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{srcname}-*.egg-info/
%{python3_sitelib}/%{srcname}/
%{_bindir}/osmtool_*
