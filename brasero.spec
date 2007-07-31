%define name	brasero
%define version	0.6.0
%define svn	0
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
Source0:	%{name}-%{svn}.tar.bz2
%else
Source0:	http://ftp.gnome.org/pub/gnome/sources/brasero/0.6/%{name}-%{version}.tar.bz2
%endif
# Enables deprecated APIs. Needed to build Brasero 0.6.0 against GTK+
# 2.11.6. See GNOME Bug #462185. Remove when fixed. -AdamW 2007/07
Patch0:		brasero-0.6.0-enable_deprecated.patch
URL:		http://www.gnome.org/projects/brasero/
License:	GPLv2
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
BuildRequires:	libgcrypt-devel
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
%patch0 -p1 -b .deprecated
# Seems to have changed in GLIBC 2.6...
perl -pi -e 's,SG_FLAG_LUN_INHIBIT,SG_FLAG_UNUSED_LUN_INHIBIT,g' src/scsi/scsi-command.c
perl -pi -e 's,SG_FLAG_LUN_INHIBIT,SG_FLAG_UNUSED_LUN_INHIBIT,g' src/scsi/scsi-sg.c

%build
%if %svn
./autogen.sh
%endif
# Needed by patch0
automake
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
%{_datadir}/icons/hicolor/*/apps/*
%exclude %{_datadir}/icons/hicolor/icon-theme.cache
%{_mandir}/man1/brasero.1*
%{_datadir}/mime/packages/brasero.xml
