%define rver	0.42-6
%define ver	%(echo %rver|tr '-' '.')

%define debug_package %{nil}

Summary:	Real-time patchable audio and multimedia processor
Name:		pd
Version:	%{ver}
Release:	2
License:	BSD
Group:		Sciences/Other
URL:		http://www.puredata.org
Source0:	http://downloads.sourceforge.net/pure-data/%{name}-%{rver}.src.tar.gz
Patch0:		pd-0.42-6-tcl86.patch
Patch1:		pd-0.42-6-big_endian.patch
Patch2:		pd-0.42-6-fix_strncpy_usage.patch
#Patch3:		pd-0.42-6-hurd.patch
Patch4:		pd-0.42-6-nostrip.patch
Patch5:		pd-0.42-6-linking.patch
BuildRequires:	tcl >= 8.5
BuildRequires:	tcl-devel >= 8.5
BuildRequires:	tk >= 8.5
BuildRequires:	pkgconfig(tk) >= 8.5
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(portaudio-2.0)
Requires:	tcl >= 8.5
Requires:	tk >= 8.5
# PD expects quite a few files from the docs to be present for various
# things to work, so there's really no point in separating them out
# - AdamW 2008/12
Obsoletes:	%{name}-doc < %{version}-%{release}

%description
Pd gives you a canvas for patching together modules that analyze, process,
and synthesize sounds, together with a rich palette of real-time control  
and I/O possibilities.  Similar to Max (Cycling74) and JMAX (IRCAM).  A   
related software package named Gem extends Pd's capabilities to include   
graphical rendering.

%package devel
Summary:	Development files for Pure Data
Group:		Development/Other

%description devel
Development files for Pure Data.

%prep
%setup -q -n %{name}-%{rver}
%patch0 -p1 -b .tcl86
%patch1 -p1 -b .big_endian
%patch2 -p1 -b .strncopy
#% patch3 -p1 -b .hurd
%patch4 -p1 -b .nostrip
%patch5 -p1 -b .linking

sed -i -e 's|doc/|share/%{name}/doc/|g' src/s_main.c src/u_main.tk
sed -i -e 's|\(^set help_top_directory\).*|\1 %{_datadir}/%{name}/doc|' src/u_main.tk

%build
pushd src
autoconf
export CPPFLAGS="%{optflags}"
%configure2_5x \
	--enable-jack \
	--enable-alsa \
	--enable-fftw \
	--enable-portaudio \
	--enable-portmidi

%make LDFLAGS="%{ldflags}"
popd

%install

%__mkdir_p %{buildroot}%{_bindir}
%__mkdir_p %{buildroot}%{_mandir}/man1
%__mkdir_p %{buildroot}%{_includedir}/%{name}
%__mkdir_p %{buildroot}%{_datadir}/%{name}

%__install -s -m 755 bin/pd %{buildroot}/%{_bindir}
%__install -s bin/pdsend bin/pdreceive %{buildroot}/%{_bindir}
%__install -s bin/pd-gui bin/pd-watchdog %{buildroot}/%{_bindir}
%__install bin/pd.tk %{buildroot}/%{_bindir}

%__install src/*.h %{buildroot}/%{_includedir}/%{name}
cp -pr doc/ %{buildroot}%{_datadir}/%{name}
%__install -m 644 man/*.1 %{buildroot}/%{_mandir}/man1


%files
%doc README.txt LICENSE.txt
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/%{name}

%files devel
%{_includedir}/%{name}


%changelog
* Thu Dec 16 2010 Jani VÃ¤limaa <wally@mandriva.org> 0.42.6-1mdv2011.0
+ Revision: 622282
- new version 0.42.6
- update P0 name
- add P1,P2,P3 and P4 from Debian
- add P5 to fix linking

  + Thierry Vignaud <tv@mandriva.org>
    - rebuild

* Mon Dec 29 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.41.4-3mdv2009.1
+ Revision: 320725
- enable fftw and portaudio support

* Sat Dec 06 2008 Adam Williamson <awilliamson@mandriva.org> 0.41.4-2mdv2009.1
+ Revision: 310976
- fix paths to the required files in /doc
- don't split out the docs, they're needed for various things to work
- rebuild for new tcl
- add tcl86.patch: fix 8.6 detection, hack/fix interp->result stuff

* Mon Aug 11 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.41.4-1mdv2009.0
+ Revision: 270775
- update to new version 0.41-4
- fix urls
- fix mixture of tabs and spaces
- spec file clean

* Wed Jul 30 2008 Thierry Vignaud <tv@mandriva.org> 0.41.0-3mdv2009.0
+ Revision: 255147
- rebuild

  + Adam Williamson <awilliamson@mandriva.org>
    - version the tcl and tk requires

* Sat Feb 09 2008 Adam Williamson <awilliamson@mandriva.org> 0.41.0-1mdv2008.1
+ Revision: 164574
- rebuild for new era and new tcl/tk
- spec clean
- new release 0.41.0

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

* Mon Dec 17 2007 Thierry Vignaud <tv@mandriva.org> 0.38.1-3mdv2008.1
+ Revision: 131080
- kill re-definition of %%buildroot on Pixel's request
- import pd


* Tue Jan 03 2006 Oden Eriksson <oeriksson@mandriva.com> 0.38.1-3mdk
- rebuilt against soname aware deps (tcl/tk)
- fix deps

* Fri Sep 30 2005 Nicolas Lécureuil <neoclust@mandriva.org> 0.38.1-2mdk
 - buildrequires fix

* Sat Jan 15 2005 Tibor Pittich <Tibor.Pittich@mandrake.org> 0.38.1-1mdk
- initial mandrakelinux import
- macroszification and some other mandrakelinux specific changes
