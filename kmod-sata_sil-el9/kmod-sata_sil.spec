# Define the kmod package name here.
%define kmod_name	sata_sil

# If kmod_kernel_version isn't defined on the rpmbuild line, define it here.
%{!?kmod_kernel_version: %define kmod_kernel_version 5.14.0-162.6.1.el9_1}

%{!?dist: %define dist .el9}

Name:		kmod-%{kmod_name}
Version:	2.4
Release:	3%{?dist}
Summary:	%{kmod_name} kernel module(s)
Group:		System Environment/Kernel
License:	GPLv2
URL:		http://www.kernel.org/

# Sources.
Source0:	drivers-ata.tar.gz
Source5:	GPL-v2.0.txt
Source7:	scsi_transport_api.h

# Fix for the SB-signing issue caused by a bug in /usr/lib/rpm/brp-strip
# https://bugzilla.redhat.com/show_bug.cgi?id=1967291

%define __spec_install_post \
		/usr/lib/rpm/check-buildroot \
		/usr/lib/rpm/redhat/brp-ldconfig \
		/usr/lib/rpm/brp-compress \
		/usr/lib/rpm/brp-strip-comment-note /usr/bin/strip /usr/bin/objdump \
		/usr/lib/rpm/brp-strip-static-archive /usr/bin/strip \
		/usr/lib/rpm/redhat/brp-python-bytecompile "" "1" "0" \
		/usr/lib/rpm/brp-python-hardlink \
		/usr/lib/rpm/redhat/brp-mangle-shebangs

# Source code patches
Patch0: elrepo-libata-eh.patch

%define findpat %( echo "%""P" )
%define __find_requires /usr/lib/rpm/redhat/find-requires.ksyms
%define __find_provides /usr/lib/rpm/redhat/find-provides.ksyms %{kmod_name} %{?epoch:%{epoch}:}%{version}-%{release}
%define dup_state_dir %{_localstatedir}/lib/rpm-state/kmod-dups
%define kver_state_dir %{dup_state_dir}/kver
%define kver_state_file %{kver_state_dir}/%{kmod_kernel_version}.%{_arch}
%define dup_module_list %{dup_state_dir}/rpm-kmod-%{kmod_name}-modules
%define debug_package %{nil}

%global _use_internal_dependency_generator 0
%global kernel_source() %{_usrsrc}/kernels/%{kmod_kernel_version}.%{_arch}

BuildRoot:			%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

ExclusiveArch:		x86_64

BuildRequires:		elfutils-libelf-devel
BuildRequires:		kernel-abi-stablelists
BuildRequires:		kernel-devel = %{kmod_kernel_version}
BuildRequires:		kernel-rpm-macros
BuildRequires:		redhat-rpm-config
BuildRequires:		rpm-build
BuildRequires:		gcc
BuildRequires:		make

Provides:			kernel-modules >= %{kmod_kernel_version}.%{_arch}
Provides:			kmod-%{kmod_name} = %{?epoch:%{epoch}:}%{version}-%{release}

Requires:			kernel >= %{kmod_kernel_version}
Requires:			kernel-core-uname-r >= %{kmod_kernel_version}

Requires(post):		%{_sbindir}/depmod
Requires(postun):	%{_sbindir}/depmod
Requires(post):		%{_sbindir}/weak-modules
Requires(postun):	%{_sbindir}/weak-modules

%description
This package provides the %{kmod_name} kernel module(s).
It is built to depend upon the specific ABI provided by a range of releases
of the same variant of the Linux kernel and not on any one specific build.

%prep
%setup -q -n drivers-ata
echo "override %{kmod_name} * weak-updates/%{kmod_name}" > kmod-%{kmod_name}.conf

%{__cp} %{SOURCE7} .

# Apply patch(es)
%patch0 -p1

%build
%{__make} -C %{kernel_source} %{?_smp_mflags} V=1 modules M=$PWD CONFIG_SATA_SIL=m

whitelist="/lib/modules/kabi-current/kabi_stablelist_%{_target_cpu}"
for modules in $( find . -name "*.ko" -type f -printf "%{findpat}\n" | sed 's|\.ko$||' | sort -u ) ; do
	# update greylist
	nm -u ./$modules.ko | sed 's/.*U //' |  sed 's/^\.//' | sort -u | while read -r symbol; do
		grep -q "^\s*$symbol\$" $whitelist || echo "$symbol" >> ./greylist
	done
done
sort -u greylist | uniq > greylist.txt

%install
%{__install} -d %{buildroot}/lib/modules/%{kmod_kernel_version}.%{_arch}/extra/%{kmod_name}/
%{__install} %{kmod_name}.ko %{buildroot}/lib/modules/%{kmod_kernel_version}.%{_arch}/extra/%{kmod_name}/
%{__install} -d %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} -m 0644 kmod-%{kmod_name}.conf %{buildroot}%{_sysconfdir}/depmod.d/
%{__install} -d %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/
%{__install} -m 0644 %{SOURCE5} %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/
%{__install} -m 0644 greylist.txt %{buildroot}%{_defaultdocdir}/kmod-%{kmod_name}-%{version}/

# strip the modules(s)
find %{buildroot} -name \*.ko -type f | xargs --no-run-if-empty %{__strip} --strip-debug

# Sign the modules(s)
%if %{?_with_modsign:1}%{!?_with_modsign:0}
	# If the module signing keys are not defined, define them here.
	%{!?privkey: %define privkey %{_sysconfdir}/pki/SECURE-BOOT-KEY.priv}
	%{!?pubkey: %define pubkey %{_sysconfdir}/pki/SECURE-BOOT-KEY.der}
	for module in $(find %{buildroot} -type f -name \*.ko);
		do %{_usrsrc}/kernels/%{kmod_kernel_version}.%{_arch}/scripts/sign-file \
			sha256 %{privkey} %{pubkey} $module;
	done
%endif

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(644,root,root,755)
/lib/modules/%{kmod_kernel_version}.%{_arch}/
%config /etc/depmod.d/kmod-%{kmod_name}.conf
%doc /usr/share/doc/kmod-%{kmod_name}-%{version}/

%changelog
* Tue Dec 20 2022 Patrick Coakley <patrick.coakley@spearline.com> - 2.4-3
- Remove %post_* sections for ostree

* Tue Nov 15 2022 Akemi Yagi <toracat@elrepo.org> - 2.4-2
- Rebuilt against RHEL 9.1 GA kernel 5.14.0-162.6.1.el9_1
- Source code from kernel-5.14.0-162.6.1.el9_1

* Tue May 17 2022 Akemi Yagi <toracat@elrepo.org> - 2.4-1
- Rebuilt against RHEL 9.0 GA kernel 5.14.0-70.13.1.el9_0
- Source code from kernel-5.14.0-70.13.1.el9_0
