%define rver	0.51-4
%define ver	%(echo %rver|tr '-' '.')

Summary:	Real-time patchable audio and multimedia processor
Name:		pd
Version:	0.25
Release:	2
License:	BSD
Group:		Sciences/Other
Url:		http://www.puredata.org
Source0:	http://msp.ucsd.edu/Software/%{name}-%{rver}.src.tar.gz
#Source0:	http://downloads.sourceforge.net/pure-data/%{name}-%{version}.src.tar.gz
Source100:	%{name}.rpmlintrc
Patch0:		pd-0.51-4-fix-symlink.patch

BuildRequires:	tcl >= 8.5
BuildRequires:	tcl-devel >= 8.5
BuildRequires:	tk >= 8.5
BuildRequires:	pkgconfig(alsa)
BuildRequires:	pkgconfig(jack)
BuildRequires:	pkgconfig(portaudio-2.0)
#BuildRequires:  portmidi-devel
BuildRequires:	pkgconfig(tk) >= 8.5
BuildRequires:	pkgconfig(fftw3)
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
%{_libdir}/pd/*
%{_mandir}/man1/*
#{_datadir}/%{name}

#----------------------------------------------------------------------------

%package devel
Summary:	Development files for Pure Data
Group:		Development/Other

%description devel
Development files for Pure Data.

%files devel
%{_includedir}/%{name}
%{_includedir}/m_pd.h
%{_libdir}/pkgconfig/pd.pc

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{rver}
%autopatch -p1

%build
./autogen.sh
export CPPFLAGS="%{optflags}"
%configure \
	--enable-jack \
	--enable-alsa \
	--disable-fftw \
	--enable-portaudio
#	--enable-portmidi

%make_build LDFLAGS="%{ldflags}"

%install
%make_install
