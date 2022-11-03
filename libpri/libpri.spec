Name:           libpri
Version:        1.6.0
%global so_version 1
Release:        13%{?dist}
Summary:        An implementation of Primary Rate ISDN

# From README:
#   As a special exception, libpri may also be linked to the OpenH323 library,
#   so long as the entirity of the derivative work (as defined within the GPL)
#   is licensed either under the MPL of the OpenH323 license or the GPL of
#   libpri.
License:        GPLv2+
URL:            https://www.asterisk.org/
%global src_base https://downloads.asterisk.org/pub/telephony/%{name}/releases
Source0:        %{src_base}/%{name}-%{version}.tar.gz
Source1:        %{src_base}/%{name}-%{version}.tar.gz.asc
# Keyring with developer signatures created on 2021-02-23 with:
#   workdir="$(mktemp --directory)"
#   gpg2 --with-fingerprint libpri-1.6.0.tar.gz.asc 2>&1 |
#     awk '$2 == "using" { print "0x" $NF }' |
#     xargs gpg2 --homedir="${workdir}" \
#         --keyserver=hkp://pool.sks-keyservers.net --recv-keys
#   gpg2 --homedir="${workdir}" --export --export-options export-minimal \
#       > libpri.gpg
#   rm -rf "${workdir}"
# Inspect keys using:
#   gpg2 --list-keys --no-default-keyring --keyring ./libpri.gpg
Source2:        %{name}.gpg

# Upstream bug PRI-186:
#   https://issues.asterisk.org/jira/browse/PRI-186
# Debian downstream bug:
#   https://bugs.debian.org/cgi-bin/bugreport.cgi?bug=957470
# Patch from Debian, which we use unmodified:
#   https://bugs.debian.org/cgi-bin/bugreport.cgi?att=1;bug=957470;filename=zero-sized-members.patch;msg=32
Patch0:         zero-sized-members.patch

BuildRequires:  gnupg2

BuildRequires:  make
BuildRequires:  gcc

BuildRequires:  dahdi-tools-devel

%global _hardened_build 1

%description
%{name} is a C implementation of the Primary Rate ISDN specification.
It was based on the Bellcore specification SR-NWT-002343 for National ISDN. As
of May 12, 2001, it has been tested work to with NI-2, Nortel DMS-100, and
Lucent 5E Custom protocols on switches from Nortel and Lucent.


%package devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use %{name}.


%package doc
Summary:        Documentation for %{name}

BuildArch:      noarch

%description doc
Currently, the %{name}-doc package contains the pseudocode for the finite state
machines used in its implementation.


%prep
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup


%build
%set_build_flags
%make_build


%install
%make_install INSTALL_BASE=%{_prefix} libdir=%{_libdir}
# Remove the static library
find %{buildroot} -name '*.a' -print -delete
# Manually fix the symlinks
fully_versioned_so="$(basename %{buildroot}/%{_libdir}/%{name}.so.%{so_version}.*)"
versioned_so="$(echo "${fully_versioned_so}" | cut -d . -f -3)"
unversioned_so="$(echo "${fully_versioned_so}" | cut -d . -f -2)"
ln -svf "${fully_versioned_so}" "%{buildroot}%{_libdir}/${versioned_so}"
ln -svf "${versioned_so}" "%{buildroot}%{_libdir}/${unversioned_so}"


%if 0%{?epel} && 0%{?epel} < 8
%ldconfig_scriptlets
%endif


%check
./rosetest
./testprilib


%files
%license LICENSE
%doc ChangeLog
%doc README
%{_libdir}/%{name}.so.%{so_version}
%{_libdir}/%{name}.so.%{so_version}.*


%files devel
%{_includedir}/%{name}.h
%{_libdir}/%{name}.so


%files doc
%license LICENSE
%doc ChangeLog
%doc README
%doc doc/*.fsm


%changelog
* Tue Feb 23 2021 Benjamin A. Beasley <code@musicinmybrain.net> - 1.6.0-13
- Trivial typo fix in description
- Add source file verification

* Thu Dec  3 2020 Benjamin A. Beasley <code@musicinmybrain.net> - 1.6.0-10
- Add ldconfig_scriptlets macro for EPEL

* Thu Dec  3 2020 Benjamin A. Beasley <code@musicinmybrain.net> - 1.6.0-9
- Reformat whitespace
- Convert URLs from HTTP to HTTPS
- Add BR on make for
  https://fedoraproject.org/wiki/Changes/Remove_make_from_BuildRoot
- Use macros to reduce repetition throughout
- Use modern macros (license, make_build/make_install)
- Make -devel dependency on main package strict (arched)
- Add -doc subpackage with finite state machine pseudocode
- Fix so version symlinking
- Add patch from Debian for upstream issue PRI-186 (libpri fails to build with
  GCC 10)
- Honor system rpm configuration build flags, including hardening flags
- Run some tests

* Sat Aug 01 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-8
- Second attempt - Rebuilt for
  https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Tue Jul 28 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Jan 29 2020 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Thu Jul 25 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Fri Feb 01 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Fri Jul 13 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.6.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Feb 19 2018 Jared Smith <jsmith@fedoraproject.org> - 1.6.0-2
- Add missing BuildRequires on gcc

* Wed Feb 14 2018 Jared Smith <jsmith@fedoraproject.org> - 1.6.0-1
- Update to upstream 1.6.0 release
- Convert to using ldconfig_scriptlets macro
- Fix invalid dates in changelog entries

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.13-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.13-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.13-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.13-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.4.13-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.13-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.13-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.13-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.13-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.13-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct  9 2012 Jeffrey Ollie <jeff@ocjtech.us> - 1.4.13-1
- The Asterisk Development Team has announced the release of libpri 1.4.13.
- This release is available for immediate download at
- http://downloads.asterisk.org/pub/telephony/libpri
-
- The release of libpri 1.4.13 resolves several issues reported by the
- community and would have not been possible without your participation.
- Thank you!
-
- The following are the issues resolved in this release:
-
- * --- Outgoing BRI calls fail when using Asterisk 1.8 with HA8, HB8,
-       and B410P cards.
-   (Issue AST-598. Reported by Trey Blancher)
-
- * --- Implement handling a multi-channel RESTART request.
-   (Closes issue PRI-93. Reported by Marcin Kowalczyk)
-
- * --- Removed MDL/TEI management configuration warning message.
-   (Closes issue PRI-137. Reported by Bart Coninckx)
-
- * --- Allow passing compiler flags (CFLAGS, LDFLAGS)
-   (Closes issue PRI-144. Reported by Tzafrir Cohen)
-
- For a full list of changes in this release, please see the ChangeLog:
-
- http://downloads.asterisk.org/pub/telephony/libpri/ChangeLog-1.4.13

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.12-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.12-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Jul  6 2011 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.12-1
- The Asterisk Development Team announces the release of libpri version
- 1.4.12.  This release is available for immediate download at
- http://downloads.asterisk.org/pub/telephony/libpri/
-
- The following are some of the issues resolved in this release:
-
-  * Add call transfer exchange of subaddresses support and fix PTMP call
-    transfer signaling.
-
-  * Invalid PTMP redirecting signaling as TE towards NT.
-
-  * Add Q931_IE_TIME_DATE to CONNECT message when in network mode.
-    (issue #18047 (JIRA PRI-114). Reported by: wuwu. Patched by rmudgett)
-
-  * Swap of master/slave in pri_enslave() incorrect.
-    (issue #18769 (JIRA PRI-120). Reported by: jcollie. Patched by jcollie)
-
-  * Fix I-frame retransmission quirks.
-
-  * Crash if NFAS swaps D channels on a call with an active timer.
-
-  * DMS-100 not receiving caller name anymore.
-    (issue #18822 (JIRA PRI-121). Reported by: cmorford. Patched by rmudgett)
-
-  * B channel lost by incoming call in BRI NT PTMP mode.
-
-  * Implement the mandatory T312 timer for NT PTMP broadcast SETUP calls.
-
- This release contains several new features, among them:
-
- 1.) ETSI and Q.SIG Call Completion Supplementary Service (CCSS) support
- 2.) ETSI Advice Of Charge (AOC) support
- 3.) ETSI Explicit Call Transfer (ECT) support
- 4.) ETSI Call Waiting support for ISDN phones
- 5.) ETSI Malicious Call ID support
- 6.) Add Display IE text handling options.
-
- For a full list of changes in this release, please see the ChangeLog:
-
- http://downloads.asterisk.org/pub/telephony/libpri/releases/ChangeLog-1.4.12

* Tue Feb  8 2011 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.12-0.3.beta3
-
- The following are some of the issues resolved in this beta release:
-
-   * Prevent a CONNECT message from sending a CONNECT ACKNOWLEDGE in the
-     wrong state.
-     (issue #17360. Reported by: shawkris. Patched by rmudgett)
-
-   * Made Q.921 delay events to Q.931 if the event could immediately
-     generate response frames.
-     (closes issue #17360. Reported by: shawkris. Patched by rmudgett)
-
-   * BRI PTMP: Active channels not cleared when the interface goes down.
-     (closes issue #17865. Reported by: wimpy. Patched by rmudgett)
-
-   * Segfault in pri_schedule_del() - ctrl value is invalid.
-     (closes issue #17522)
-     (closes issue #18032. Reported by: schmoozecom. Patched by rmudgett)
-
-   * Crash when receiving an unknown/unsupported message type.
-     (closes issue #17968. Reported by: gelo. Patched by rmudgett)
-
-   * B410P gets incoming call packets on ISDN but Asterisk doesn't see the
-     call.
-     (closes issue #18232. Reported by: lelio. Patched by rmudgett)
-
-   * SABME flood on backup D-channel in NFAS configuration.
-     (closes issue #18255. Reported by: bklang. Patched by rmudgett)
-
-   * Asterisk is getting a "No D-channels available!" warning message every
-     4 seconds.
-     (closes issue #17270. Reported by: jmls. Patched by rmudgett)
-
- This beta release contains several new features, among them:
-
- 1.) ETSI and Q.SIG Call Completion Supplementary Service (CCSS) support
- 2.) ETSI Advice Of Charge (AOC) support
- 3.) ETSI Explicit Call Transfer (ECT) support
- 4.) ETSI Call Waiting support for ISDN phones
- 5.) ETSI Malicious Call ID support
-
- For a full list of changes in the current release candidate, please see
- the ChangeLog:
-
- http://downloads.asterisk.org/pub/telephony/libpri/releases/ChangeLog-1.4.12-beta3

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.12-0.2.beta2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Oct  8 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.12-0.2.beta2
- The following are some of the issues resolved in this beta release:
-
-   * Fix issue where calling name is not successfully processed on inbound
-     QSIG PRI calls from Mitel PBX.
-     (Closes issue #17619. Reported by: jims8650. Patched by rmudgett)
-
-   * Added missing code specified by Q.921 (Figure B.8 Page 85) when receive
-     RNR in "Timer Recovery" state.
-     (Closes issue #16791. Reported by: alecdavis. Patched by alecdavis)
-
-   * Fixed issue where incoming calls specifying the channel using a slot
-     map could not negotiate a B channel correctly.
-
-   * Add support to receive ECMA-164 2nd edition OID name ROSE messages.
-
-   * Fixed issue where ISDN BRI PTMP TE does not recover from line faults.
-     (Closes issue #17570. Reported by: jcovert. Patched by rmudgett)
-
-   * Q.921 improvements from comparing Q.921 SDL diagrams with implementation.
-
-   * Q.921/Q.931 message debug output improvements.
-
- This beta release contains several new features, among them:
-
- 1.) ETSI and Q.SIG Call Completion Supplementary Service (CCSS) support
- 2.) ETSI Advice Of Charge (AOC) support
- 3.) ETSI Explicit Call Transfer (ECT) support
- 4.) ETSI Call Waiting support for ISDN phones
- 5.) ETSI Malicious Call ID support
-
- For a full list of changes in the current release candidate, please see
- the ChangeLog:
-
- http://downloads.asterisk.org/pub/telephony/libpri/releases/ChangeLog-1.4.12-beta2

* Mon Aug  2 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.12-0.1.beta1
- 1.4.12-beta1
-
- This beta release contains some fixes and several new features, among them:
-
- 1.) ETSI and Q.SIG Call Completion Supplementary Service (CCSS) support
-
- 2.) ETSI Advice Of Charge (AOC) support
-
- 3.) ETSI Explicit Call Transfer (ECT) support
-
- 4.) ETSI Call Waiting support for ISDN phones
-
- 5.) ETSI Malicious Call ID support
-
- For a full list of changes in the current release candidate, please see
- the ChangeLog:
-
- http://downloads.asterisk.org/pub/telephony/libpri/releases/ChangeLog-1.4.12-beta1

* Mon Aug  2 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.11.3-1
- 1.4.11.3:
- This release fixes a regression in the calling number assignment logic:
-
-  * Calling Number assignment logic change in libpri 1.4.11. Restored the old
-    behaviour if there is more than one calling number in the incoming SETUP
-    message.  A network provided number is reported as ANI.
-    (Closes issue #17495. Reported and tested by ibercom. Patched by rmudgett)
-
- For a full list of changes in the current release, please see the ChangeLog:
-
- http://downloads.asterisk.org/pub/telephony/libpri/releases/ChangeLog-1.4.11.3

* Thu Jun 10 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.11.2-1
- 1.4.11.2:
-
- This release fixes situation where Q.SIG calling name in FACILITY
- message was not reported to the upper layer:
-
- * pri_facility.c: Q.SIG calling name in FACILITY message not reported
-   to the upper layer. Q.SIG can send the CallingName, CalledName, and
-   ConnectedName in stand alone FACILITY messages.  If the CallingName
-   was not sent in the SETUP message, the caller id name was not
-   reported to the upper layer.  (Closes issue #17458. Reported, tested
-   by: jsmith. Patched by rmudgett)
-
- For a full list of changes in the current release, please see the
- ChangeLog:
-
- http://downloads.asterisk.org/pub/telephony/libpri/releases/ChangeLog-1.4.11.2
-
- 1.4.11.1:
-
- This release fixes a regression in multi component FACILITY messages
- and includes a minor bug fix for BRI spans:
-
- * Multi component FACILITY messages only process the first
-   component. The code was only processing the first ROSE component in
-   the facility message.  (Closes issue #17428. Reported, tested by:
-   patrol-cz. Patched by rmudgett)
-
- * Inband disconnect setting does nothing on BRI spans.  The
-   acceptinbanddisconnect flag is not inherited when creating a new TEI
-   and thus rendering the setting (and its respective equivalent in
-   Asterisk) a no-op on BRI setups.  (Closes issue #15265. Reported,
-   patched, tested by: paravoid)
-
- For a full list of changes in the current release, please see the
- ChangeLog:
-
- http://downloads.asterisk.org/pub/telephony/libpri/releases/ChangeLog-1.4.11.1

* Wed May 26 2010 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.11-1
- This release contains many fixes and new features, among them being:
-
- 1.) Support for NT-PTMP BRI links, including support for multiple TEIs
- and connecting of BRI phones.
-
- 2.) Support for allowing persistent Q.921 drops on both NT and TE PTMP
- links, as well as automatically requesting that Q.921 data links
- reactivate when needed by Q.931.
-
- 3.) T309 is enabled by default.
-
- 4.) Problems with Keypad Facility Digits were addressed.
-
- 5.) A number of additional service related features were added:
- Connected Line Information, HOLD/RELEASE support, Call Deflection/Call
- Rerouting, as well as partial subaddress support.  They are supported in
- the Q.SIG and EuroISDN switch types, and most currently require using
- the trunk version of Asterisk.
-
- 6.) Many potential and realized Q.921 related problems, particularly
- during retransmissions and other scenarios involving medium to high
- packet loss.
-
- For a full list of changes in the current release candidates, please see
- the ChangeLog:
-
- http://downloads.asterisk.org/pub/telephony/libpri/releases/ChangeLog-1.4.11

* Tue Oct 20 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.10.2-1
- Update to libpri 1.4.10.2

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Fri Apr 24 2009 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.10-1
- Update to 1.4.10

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.7-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Tue Aug  5 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.7-1
- Update to 1.4.7

* Tue Jul 29 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.6-1
- Update to 1.4.6

* Mon Feb 11 2008 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.3-2
- Rebuild for GCC 4.3

* Thu Dec 20 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.3-1
- Update to 1.4.3.
- Drop upstreamed patch.

* Thu Nov  1 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.2-1
- Update to 1.4.2

* Wed Aug 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.1-5
- Bump release.

* Wed Aug 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.1-4
- Add patch to define size_t

* Wed Aug 29 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.1-3
- Update license tag.
- Update URL.

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 1.4.1-2
- Rebuild for selinux ppc32 issue.

* Mon Jul  9 2007 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.1-1
- Update to 1.4.1

* Sat Dec 23 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.0-3
- Update to 1.4.0 final

* Sat Oct 14 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.0-2.beta1
- Fix lib paths for 64 bit systems.

* Sat Oct 14 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.0-1.beta1
- Get rid of pesky "." in -devel summary.
- Remove zaptel-devel BR

* Fri Oct 13 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.0-1.beta1
- devel package needs to Require: main package

* Fri Oct 13 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.4.0-0.beta1
- Update to 1.4.0-beta1

* Fri Jun  2 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.2.3
- Update to 1.2.3
- Add dist tag to release
- Update source URL

* Wed Jan 18 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.2.2-1
- Update to 1.2.2.
- Fix the spelling of Paul Komkoff Jr.'s name.

* Fri Jan 13 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.2.1-4
- Eliminate the libpri-install.patch and other improvements based on suggestions from Paul Komkoff Jr.

* Thu Jan 12 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.2.1-3
- Fix building on 64 bit systems.

* Thu Jan 12 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.2.1-2
- Changed buildroot to meet FE packaging guidelines
- Don't forget docs
- Modify %%post so that ldconfig dep will be picked up automatically
- Add %%postun so that ldconfig gets run on uninstall
- Don't package the static library
- Changed $RPM_BUILD_ROOT to %%{buildroot} (yes, I know I was consistent before, but I prefer %%{buildroot})

* Wed Jan 11 2006 Jeffrey C. Ollie <jeff@ocjtech.us> - 1.2.1-1
- First version for Fedora Extras
