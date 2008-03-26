%define branch	07
%define svn	693
%define rel	1
%if %svn
%define release		%mkrel 0.%svn.%rel
%define distname	%name%branch-%svn.tar.lzma
%define dirname		%name%branch
%else
%define release		%mkrel %rel
%define distname	%name-%version.tar.gz
%define dirname		%name-%version
%endif

Name: 	 	brasero
Summary: 	A disc burning application for GNOME
Version: 	0.7.2
Release: 	%{release}
# For SVN: svn co http://svn.gnome.org/svn/brasero/branches/brasero_0_7 brasero07
Source0:	http://ftp.gnome.org/pub/gnome/sources/brasero/0.7/%{distname}
# From upstream SVN head, per #39392
Source1:	nl.po
Patch0:		brasero-693-nl.patch
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
%setup -q -n %{dirname}
%patch0 -p1 -b .nl
install -m 0644 %{SOURCE1} po/nl.po

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
  --add-category="DiscBurning" \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/*

%find_lang %{name}

%clean
rm -rf %{buildroot}

%define schemas %{name}

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
%{_mandir}/man1/%{name}.1*
%{_datadir}/mime/packages/%{name}.xml

