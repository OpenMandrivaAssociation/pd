%define rver	0.42-6
%define ver	%(echo %rver|tr '-' '.')
%define rel	1

Summary:	Real-time patchable audio and multimedia processor
Name:		pd
Version:	%{ver}
Release:	%mkrel %{rel}
License:	BSD
Group:		Sciences/Other
URL:		http://www.puredata.org
Source0:	http://downloads.sourceforge.net/pure-data/%{name}-%{rver}.src.tar.gz
Patch0:		pd-0.42-6-tcl86.patch
Patch1:		pd-0.42-6-big_endian.patch
Patch2:		pd-0.42-6-fix_strncpy_usage.patch
Patch3:		pd-0.42-6-hurd.patch
Patch4:		pd-0.42-6-nostrip.patch
Patch5:		pd-0.42-6-linking.patch
BuildRequires:	tcl >= 8.5
BuildRequires:	tcl-devel >= 8.5
BuildRequires:	tk >= 8.5
BuildRequires:	tk-devel >= 8.5
BuildRequires:	jackit-devel
BuildRequires:	libalsa-devel
#BuildRequires:	fftw3-devel
BuildRequires:	portaudio-devel
Requires:	tcl >= 8.5
Requires:	tk >= 8.5
# PD expects quite a few files from the docs to be present for various
# things to work, so there's really no point in separating them out
# - AdamW 2008/12
Obsoletes:	%{name}-doc < %{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

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
%patch3 -p1 -b .hurd
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
rm -rf %{buildroot}

%__mkdir_p %{buildroot}%{_bindir}
%__mkdir_p %{buildroot}%{_mandir}/man1
%__mkdir_p %{buildroot}%{_includedir}/%{name}
%__mkdir_p %{buildroot}%{_datadir}/%{name}

%__install -s -m 755 bin/pd %{buildroot}/%{_bindir}
%__install -s bin/pdsend bin/pdreceive %{buildroot}/%{_bindir}
%__install -s bin/pd-gui bin/pd-watchdog %{buildroot}/%{_bindir}
%__install bin/pd.tk %{buildroot}/%{_bindir}

%__install src/*.h %{buildroot}/%{_includedir}/%{name}
%__cp -pr doc/ %{buildroot}%{_datadir}/%{name}
#%__cp -pr extra %{buildroot}/%{_libdir}/%{name}/pd

%__install -m 644 man/*.1 %{buildroot}/%{_mandir}/man1

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.txt LICENSE.txt
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/%{name}

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}
