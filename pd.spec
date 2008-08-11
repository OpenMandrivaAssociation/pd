%define rver 0.41-4

Summary:	Real-time patchable audio and multimedia processor
Name:		pd
Version:	%(echo %rver|tr '-' '.')
Release:	%mkrel 1
License:	BSD
Group:		Sciences/Other
URL:		http://www.puredata.org
Source:		http://downloads.sourceforge.net/pure-data/%{name}-%{rver}.src.tar.gz
BuildRequires:	tcl >= 8.5
BuildRequires:	tcl-devel >= 8.5
BuildRequires:	tk >= 8.5
BuildRequires:	tk-devel >= 8.5
BuildRequires:	X11-devel
BuildRequires:	jackit-devel
BuildRequires:	libalsa-devel
Requires:	tcl >= 8.5
Requires:	tk >= 8.5
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Pd gives you a canvas for patching together modules that analyze, process,
and synthesize sounds, together with a rich palette of real-time control  
and I/O possibilities.  Similar to Max (Cycling74) and JMAX (IRCAM).  A   
related software package named Gem extends Pd's capabilities to include   
graphical rendering.

%package doc
Summary:	Documentation files for Pure Data
Group:		Sciences/Other

%description doc
Documentation files for Pure Data.

%package devel
Summary:	Development files for Pure Data
Group:		Development/Other

%description devel
Development files for Pure Data.

%prep
%setup -q -n %{name}-%{rver}

%build
pushd src
%configure2_5x \
	--enable-jack \
	--enable-alsa

%make
popd

%install
rm -rf %{buildroot}

%__mkdir_p %{buildroot}/%{_bindir}
%__mkdir_p %{buildroot}/%{_mandir}/man1
%__mkdir_p %{buildroot}/%{_includedir}/%{name}

%__install -s -m 755 bin/pd %{buildroot}/%{_bindir}
%__install -s bin/pdsend bin/pdreceive %{buildroot}/%{_bindir}
%__install -s bin/pd-gui bin/pd-watchdog %{buildroot}/%{_bindir}
%__install bin/pd.tk %{buildroot}/%{_bindir}

%__install src/*.h %{buildroot}/%{_includedir}/%{name}
#%__cp -pr extra %{buildroot}/%{_libdir}/%{name}/pd

%__install -m 644 man/* %{buildroot}/%{_mandir}/man1

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README.txt LICENSE.txt
%{_bindir}/*
%{_mandir}/man1/*

# TODO
# path to tesstone.pd is hardcoded in u_main.tk
%files doc
%defattr(-,root,root)
%doc doc

%files devel
%defattr(-,root,root)
%dir %{_includedir}/%{name}
%{_includedir}/%{name}
