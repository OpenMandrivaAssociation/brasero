%define name	brasero
%define version	0.6.0
%define svn	245
%if %svn
%define release %mkrel 0.%svn.1
%else
%define release %mkrel 1
%endif

Name: 	 	%{name}
Summary: 	A disc burning application for GNOME
Version: 	%{version}
Release: 	%{release}

%if %svn
Source:		%{name}-%{svn}.tar.bz2
%else
Source:		http://perso.wanadoo.fr/bonfire/%{name}-%{version}.tar.bz2
%endif
URL:		http://perso.wanadoo.fr/bonfire/
License:	GPL
Group:		Archiving/Cd burning
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	ImageMagick
BuildRequires:	libgnome-vfs2-devel
BuildRequires:	libnautilus-burn-devel
BuildRequires:	libgstreamer0.10-devel
BuildRequires:	libxml2-devel
BuildRequires:	perl-XML-Parser
BuildRequires:	libbeagle-devel >= 0.2.5
BuildRequires:	totem-plparser-devel
BuildRequires:	libgdl-devel >= 0.6
BuildRequires:	libnotify-devel
BuildRequires:  desktop-file-utils
BuildRequires:	libgstreamer0.10-plugins-base-devel
BuildRequires:	libburn-devel
BuildRequires:	libisofs-devel
%if %svn
BuildRequires:	autoconf
BuildRequires:	gnome-common
BuildRequires:	intltool
%endif
Requires:	hal >= 0.5.0

Obsoletes:	bonfire
Provides:	bonfire

Requires(post): desktop-file-utils 
Requires(postun): desktop-file-utils

%description
Bonfire is yet another application to burn CD/DVD for the gnome desktop. It is
designed to be as simple as possible and has some unique features to enable
users to create their discs easily and quickly.

%prep
%if %svn
%setup -q -n %{name}
%else
%setup -q
%endif

%build
%if %svn
./autogen.sh
%endif
%configure2_5x --disable-schemas-install --disable-caches
%make
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

#menu

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="" \
  --remove-category="X-GNOME-Bugzilla-Bugzilla" \
  --remove-category="X-GNOME-Bugzilla-Product" \
  --remove-category="X-GNOME-Bugzilla-Component" \
  --add-category="DiscBurning;" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%define schemas %name

%post
%post_install_gconf_schemas %{schemas}
%update_menus
%update_desktop_database
%update_mime_database
%update_icon_cache hicolor

%preun
%preun_uninstall_gconf_schemas %{schemas}
		
%postun
%clean_menus
%clean_desktop_database
%clean_mime_database
%clean_icon_cache hicolor

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog MAINTAINERS NEWS README
%{_sysconfdir}/gconf/schemas/%name.schemas
%{_bindir}/%name
%{_datadir}/applications/*
%{_datadir}/%name
#%{_datadir}/pixmaps/*
%{_datadir}/icons/hicolor/*/apps/*
%exclude %{_datadir}/icons/hicolor/icon-theme.cache
#%{_datadir}/icons/gnome/48x48/mimetypes/gnome-mime-application-x-brasero.png
%{_mandir}/man1/brasero.1.bz2
%{_datadir}/mime/packages/brasero.xml


