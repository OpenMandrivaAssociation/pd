%define rver	0.51-3
%define ver	%(echo %rver|tr '-' '.')

Summary:	Real-time patchable audio and multimedia processor
Name:		pd
Version:	%{ver}
Release:	1
License:	BSD
Group:		Sciences/Other
Url:		http://www.puredata.org
Source0:	http://msp.ucsd.edu/Software/%{name}-%{rver}.src.tar.gz
#Source0:	http://downloads.sourceforge.net/pure-data/%{name}-%{version}.src.tar.gz
Source100:	%{name}.rpmlintrc
#Patch0:		pd-0.42-6-tcl86.patch
#Patch1:		pd-0.42-6-big_endian.patch
#Patch2:		pd-0.42-6-fix_strncpy_usage.patch
#Patch3:		pd-0.42-6-hurd.patch
#Patch4:		pd-0.42-6-nostrip.patch
#Patch5:		pd-0.42-6-linking.patch
BuildRequires:	tcl >= 8.5
BuildRequires:	tcl-devel >= 8.5
BuildRequires:	tk >= 8.5
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(portaudio-2.0)
BuildRequires:	pkgconfig(tk) >= 8.5
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

%files
%doc README.txt LICENSE.txt
%{_bindir}/*
%{_mandir}/man1/*
%{_datadir}/%{name}

#----------------------------------------------------------------------------

%package devel
Summary:	Development files for Pure Data
Group:		Development/Other

%description devel
Development files for Pure Data.

%files devel
%{_includedir}/%{name}

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{rver}

sed -i -e 's|doc/|share/%{name}/doc/|g' src/s_main.c src/u_main.tk
sed -i -e 's|\(^set help_top_directory\).*|\1 %{_datadir}/%{name}/doc|' src/u_main.tk

%build
pushd src
autoreconf
export CPPFLAGS="%{optflags}"
%configure2_5x \
	--enable-jack \
	--enable-alsa \
	--disable-fftw \
	--enable-portaudio \
	--enable-portmidi

%make LDFLAGS="%{ldflags}"
popd

%install
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1
mkdir -p %{buildroot}%{_includedir}/%{name}
mkdir -p %{buildroot}%{_datadir}/%{name}

install -m 755 bin/pd %{buildroot}/%{_bindir}
install bin/pdsend bin/pdreceive %{buildroot}/%{_bindir}
install bin/pd-gui bin/pd-watchdog %{buildroot}/%{_bindir}
install bin/pd.tk %{buildroot}/%{_bindir}

install src/*.h %{buildroot}/%{_includedir}/%{name}
cp -pr doc/ %{buildroot}%{_datadir}/%{name}
install -m 644 man/*.1 %{buildroot}/%{_mandir}/man1

