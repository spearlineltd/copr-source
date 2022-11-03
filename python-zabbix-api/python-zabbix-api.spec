%global srcname zabbix-api
%global commit 721dba6986f39bc10b14afeb484132fb9644d28a

Name:           python-zabbix-api
Version:        0.5.4
Release:        1%{?dist}
Summary:        Zabbix-api is a Python module for working with the Zabbix API

# license is in README.markdown
License:        LGPLv2.1+
URL:            https://github.com/gescheit/scripts
Source0:        https://github.com/gescheit/scripts/archive/%{commit}/%{srcname}-%{commit}.tar.gz#/%{srcname}-%{commit}.tar.gz
BuildArch:      noarch
BuildRequires:  python3
BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
            


%?python_enable_dependency_generator  

%description
%{summary}.


%package -n python3-%{srcname}
Summary:        Zabbix-api is a Python module for working with the Zabbix API
License:        LGPLv2
Requires:       python3-requests
%{?python_provide:%python_provide python3-%{srcname}}


%description -n python3-%{srcname}
%{summary}.


%prep
%autosetup -n scripts-%{commit}

%build
cd zabbix
%py3_build


%install
cd zabbix
%py3_install


%files -n python3-%{srcname}
%doc README.md zabbix/examples/
%{python3_sitelib}/zabbix_api.py
%{python3_sitelib}/__pycache__/zabbix_api.cpython-%{python3_version_nodots}{,.opt-?}.pyc
%{python3_sitelib}/zabbix_api-{%version}-py3.?.egg-info/


%changelog
* Mon Apr 27 2020 Jonathan Dieter <jonathan.dieter@spearline.com> - 0.5.4-1
- Initial build

