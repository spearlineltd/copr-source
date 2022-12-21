%if 0%{?el8}
# If kmod_kernel_version isn't defined on the rpmbuild line, define it here.
%{!?kmod_kernel_version: %define kmod_kernel_version 4.18.0-372.9.1.el8}
%endif 

%if 0%{?el9}
# If kmod_kernel_version isn't defined on the rpmbuild line, define it here.
%{!?kmod_kernel_version: %define kmod_kernel_version 5.14.0-162.6.1.el9_1}
%endif 

Name:		dahdi-linux
Version:	3.2.0
Release:	1%{?dist}
Summary:	DAHDI telephony interface tools
Group:		System Environment/Kernel
License:	GPLv2
URL:		http://www.kernel.org/

# Sources
Source0:	%{name}-complete-%{version}+%{version}.tar.gz

# Source code patches
Patch0: kernel_5.14.patch

BuildRequires:	redhat-rpm-config
BuildRequires:	autoconf
BuildRequires:	libtool
Requires:	dracut
Requires:	udev
Requires:	perl
Obsoletes:	dahdi-tools <= 2.11.1
Obsoletes:	dahdi-tools-libs <= 2.11.1
Provides:	dahdi-tools == 3.2.0
Provides:	dahdi-tools-libs == 3.2.0

%description
DAHDI stands for Digium Asterisk Hardware Device Interface. This
package contains the user-space tools to configure the kernel modules
included in the package kmod-dahdi-linux

%package devel
Summary:	DAHDI telephony interface tools development libraries
Requires:	%{name} == %{version}-%{release}
Obsoletes:	dahdi-tools-devel <= 2.11.1
Provides:	dahdi-tools-devel == 3.2.0

%description devel
This package contains the libraries for dahdi-linux

%prep
%setup -n %{name}-complete-%{version}+%{version}

# Apply patch(es)
%patch0 -p1

%build
cd tools
autoreconf -i
%{configure} --with-dahdi=../linux
%{__make}
cd ..

%install
cd linux
HOTPLUG_FIRMWARE=yes DESTDIR=%{buildroot} %{__make} install-include
cd ..
cd tools
DESTDIR=%{buildroot} %{__make} install
cd ..

# Remove static libraries
rm %{buildroot}%{_libdir}/*.la %{buildroot}%{_libdir}/*.a -f

# Move perl libraries to correct location
%if 0%{?el8}
mv %{buildroot}/usr/local/share/perl5 %{buildroot}%{_datadir}/perl5
%endif 

%if 0%{?el9}
mv %{buildroot}/usr/local/share/perl5/5.32 %{buildroot}%{_datadir}/perl5
%endif 

%files
%{_datadir}/dahdi
%{_datadir}/perl5/Dahdi.pm
%{_datadir}/perl5/Dahdi
%{_libdir}/libtonezone.so.2*
%{_mandir}/man8/*
%{_prefix}/lib/dracut/dracut.conf.d/*
%{_sbindir}/*
%{_sysconfdir}/dahdi
%{_sysconfdir}/bash_completion.d/dahdi
%{_sysconfdir}/udev/*

%files devel
%{_includedir}/dahdi
%{_libdir}/libtonezone.so

%changelog
* Tue Oct 25 2022 Patrick Coakley <patrick.coakley@spearline.com> - 3.2.0-1
- Upgraded Dahdi version and trying to build for el9

* Thu Jul 01 2021 Jonathan Dieter <jonathan.dieter@spearline.com> - 3.1.0-3
- Add missing perl bindings, required for some of the binaries

* Wed Jun 30 2021 Jonathan Dieter <jonathan.dieter@spearline.com> - 3.1.0-2
- Move firmware into kmod package

* Tue Aug 25 2020 Jonathan Dieter <jonathan.dieter@spearline.com> - 3.1.0-1
- Initial build