%define name	brasero
%define version	0.7.1
%define svn	0
%define rel	2
%if %svn
%define release %mkrel 0.%svn.%rel
%else
%define release %mkrel %rel
%endif

Name: 	 	%{name}
Summary: 	A disc burning application for GNOME
Version: 	%{version}
Release: 	%{release}

%if %svn
Source0:	%{name}-%{svn}.tar.bz2
%else
Source0:	http://ftp.gnome.org/pub/gnome/sources/brasero/0.7/%{name}-%{version}.tar.gz
%endif
URL:		http://www.gnome.org/projects/brasero/
License:	GPLv2+
Group:		Archiving/Cd burning
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	ImageMagick
BuildRequires:	libgnome-vfs2-devel
BuildRequires:	libnautilus-burn-devel
BuildRequires:	gstreamer0.10-devel
BuildRequires:	libxml2-devel
BuildRequires:	perl(XML::Parser)
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
Brasero is yet another CD / DVD writing application for the GNOME
desktop. It is designed to be as simple as possible and has some
unique features to enable users to create their discs easily and
quickly. It can handle both audio and data discs, and can use either
cdrkit or libburn / libisofs as the writing backend.

%prep
%if %svn
%setup -q -n %{name}
%else
%setup -q
%endif
# fix incorrect separator
sed -i -e 's,:,;,g' data/brasero.desktop.in.in

%build
%if %svn
./autogen.sh
%endif
%configure2_5x --disable-schemas-install --disable-caches
%make

%install
rm -rf %{buildroot}
%makeinstall_std

#menu
desktop-file-install \
  --remove-category="Application" \
  --remove-category="" \
  --remove-category="X-GNOME-Bugzilla-Bugzilla" \
  --remove-category="X-GNOME-Bugzilla-Product" \
  --remove-category="X-GNOME-Bugzilla-Component" \
  --add-category="DiscBurning" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%find_lang %name

%clean
rm -rf %{buildroot}

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
%doc AUTHORS MAINTAINERS NEWS README
%{_sysconfdir}/gconf/schemas/%name.schemas
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_datadir}/applications/*
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/apps/*
%{_mandir}/man1/brasero.1*
%{_datadir}/mime/packages/brasero.xml
