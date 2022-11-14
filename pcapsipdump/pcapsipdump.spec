Summary: PCAP SIP Dump tool
Name: pcapsipdump
Distribution: RedHat
Version: 0.3
Release: 3
License: GPLv2
Source: https://github.com/denyspozniak/test/raw/master/pcapsipdump-0.3.tar.gz

BuildRequires:	gcc gcc-c++ make libpcap-devel redhat-rpm-config glib2-devel libbsd-devel

%description
pcapsipdump is a tool for dumping SIP sessions (+RTP
traffic, if available) to disk in a fashion similar
to "tcpdump -w" (format is exactly the same), but one
file per sip session (even if there is thousands of
concurrent SIP sessions).

%prep
%setup

%build
RELEASEFLAGS="-g -O3 -Wall" make

%install
mkdir -p $RPM_BUILD_ROOT/usr/sbin $RPM_BUILD_ROOT/etc/sysconfig $RPM_BUILD_ROOT/etc/rc.d/init.d $RPM_BUILD_ROOT/var/spool
make DESTDIR=$RPM_BUILD_ROOT install

%post
chkconfig pcapsipdump --add

%files
%config(noreplace) %attr(0755,root,root) /etc/sysconfig/pcapsipdump
%attr(0700,root,root) %dir    /var/spool/pcapsipdump
%attr(0755,root,root)       /etc/rc.d/init.d/pcapsipdump
%attr(0755,root,root)      /usr/sbin/pcapsipdump

%changelog
* Mon Feb 03 2020 Jonathan Dieter <jonathan.dieter@spearline.com> - 0.3-3
- Add missing BRs
- Add debug flags
