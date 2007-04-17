%define name	brasero
%define version	0.5.90
%define release %mkrel 1

Name: 	 	%{name}
Summary: 	A disc burning application for GNOME2
Version: 	%{version}
Release: 	%{release}

Source:		http://perso.wanadoo.fr/bonfire/%{name}-%{version}.tar.bz2
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
%setup -q -n %{name}-%{version}

%build
%configure2_5x --disable-schemas-install --disable-caches
%make
										
%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

#menu
mkdir -p $RPM_BUILD_ROOT%{_menudir}
cat << EOF > $RPM_BUILD_ROOT%{_menudir}/%{name}
?package(%{name}): command="%{name}" icon="%{name}.png" needs="x11" title="Bonfire" longtitle="GNOME-Integrated CD Burning" section="System/Archiving/CD Burning" xdg="true"
EOF

desktop-file-install --vendor="" \
  --remove-category="Application" \
  --remove-category="" \
  --remove-category="X-GNOME-Bugzilla-Bugzilla" \
  --remove-category="X-GNOME-Bugzilla-Product" \
  --remove-category="X-GNOME-Bugzilla-Component" \
  --add-category="X-MandrivaLinux-System-Archiving-CDBurning;DiscBurning;" \
  --dir $RPM_BUILD_ROOT%{_datadir}/applications $RPM_BUILD_ROOT%{_datadir}/applications/*

#icons
mkdir -p $RPM_BUILD_ROOT/%_liconsdir
convert -size 48x48 data/logo.png $RPM_BUILD_ROOT/%_liconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_iconsdir
convert -size 32x32 data/logo.png $RPM_BUILD_ROOT/%_iconsdir/%name.png
mkdir -p $RPM_BUILD_ROOT/%_miconsdir
convert -size 16x16 data/logo.png $RPM_BUILD_ROOT/%_miconsdir/%name.png

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%define schemas %name

%post
%post_install_gconf_schemas %{schemas}
%update_menu
%update_desktop_database
%update_mime_database
%update_icon_cache gnome

%preun
%preun_uninstall_gconf_schemas %{schemas}
		
%postun
%clean_menu
%clean_desktop_database
%clean_mime_database
%clean_icon_cache gnome

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS ChangeLog MAINTAINERS NEWS README
%{_sysconfdir}/gconf/schemas/%name.schemas
%{_bindir}/%name
%{_datadir}/applications/*
%{_datadir}/%name
#%{_datadir}/pixmaps/*
%{_datadir}/icons/hicolor/*
%exclude %{_datadir}/icons/hicolor/icon-theme.cache
%{_menudir}/%name
%{_liconsdir}/%name.png
%{_iconsdir}/%name.png
%{_miconsdir}/%name.png
#%{_datadir}/icons/gnome/48x48/mimetypes/gnome-mime-application-x-brasero.png
%{_mandir}/man1/brasero.1.bz2
%{_datadir}/mime/packages/brasero.xml


