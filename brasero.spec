%define rel	1
%define release		%mkrel %rel
%define distname	%name-%version.tar.bz2
%define dirname		%name-%version

%define major 0
%define libname %mklibname %name %major
%define develname %mklibname -d %name

Name: 	 	brasero
Summary: 	A disc burning application for GNOME
Version: 	2.29.92
Release: 	%{release}
Source0:	http://ftp.gnome.org/pub/GNOME/sources/brasero/%{distname}
Patch:		brasero-2.29.3-fix-format-strings.patch
URL:		http://www.gnome.org/projects/brasero/
License:	GPLv2+
Group:		Archiving/Cd burning
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	imagemagick
BuildRequires:	libgstreamer-devel >= 0.10.15
BuildRequires:	libxml2-devel >= 2.6.0
BuildRequires:	nautilus-devel >= 2.22.2
BuildRequires:	libbeagle-devel >= 0.3.0
BuildRequires:	libGConf2-devel
BuildRequires:	totem-plparser-devel >= 2.22.0
BuildRequires:	libgdl-devel >= 0.6
BuildRequires:	dbus-glib-devel >= 0.7.2
BuildRequires:	libgstreamer0.10-plugins-base-devel >= 0.10.0
BuildRequires:	unique-devel
BuildRequires:	libcanberra-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gir-repository
#BuildRequires:	libburn-devel
#BuildRequires:	libisofs-devel
BuildRequires:	gnome-doc-utils
BuildRequires:	gtk-doc >= 1.12
BuildRequires:	intltool >= 0.35.0
BuildRequires:	gnome-common

Obsoletes:	bonfire nautilus-cd-burner
Provides:	bonfire nautilus-cd-burner

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils

# optional requirements to make video projects work
Suggests:	vcdimager
Suggests:	dvdauthor
Suggests:	gstreamer0.10-plugins-bad

%description
Brasero is yet another CD / DVD writing application for the GNOME
desktop. It is designed to be as simple as possible and has some
unique features to enable users to create their discs easily and
quickly. It can handle both audio and data discs, and can use either
cdrkit or libburn / libisofs as the writing backend.

%package -n %libname
Group: System/Libraries
Summary: A disc burning application for GNOME - shared library

%description -n %libname
Brasero is yet another CD / DVD writing application for the GNOME
desktop. It is designed to be as simple as possible and has some
unique features to enable users to create their discs easily and
quickly. It can handle both audio and data discs, and can use either
cdrkit or libburn / libisofs as the writing backend.

%package -n %develname
Summary: A disc burning application for GNOME - development library
Group: Development/C
Requires: %libname = %version-%release
Provides: %name-devel = %version-%release
Provides: lib%name-devel = %version-%release

%description -n %develname
Brasero is yet another CD / DVD writing application for the GNOME
desktop. It is designed to be as simple as possible and has some
unique features to enable users to create their discs easily and
quickly. It can handle both audio and data discs, and can use either
cdrkit or libburn / libisofs as the writing backend.

%prep
%setup -q -n %{dirname}
%patch -p1 -b .fix-format-strings

%build
# libburn backend disabled for now (0.8.1 2008/08), it's not working;
# will restore when upstream advises it - AdamW
%configure2_5x --disable-schemas-install \
               --disable-caches \
               --enable-libburnia=no \
               --enable-gtk-doc
%make LIBS=-lm

%install
rm -rf %{buildroot}
%makeinstall_std

%find_lang %{name} --with-gnome

for omf in %{buildroot}%{_datadir}/omf/%{name}/%{name}-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/brasero-// -e s/.omf//)) $(echo $omf|sed -e s!%buildroot!!)" >> %{name}.lang
done

%clean
rm -rf %{buildroot}

%define schemas %{name}

%if %mdkversion < 200900
%post
%post_install_gconf_schemas %{schemas}
%update_mime_database
%endif

%preun
%preun_uninstall_gconf_schemas %{schemas}

%if %mdkversion < 200900
%postun
%clean_mime_database
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS MAINTAINERS NEWS README
%{_sysconfdir}/gconf/schemas/%{name}.schemas
%{_bindir}/%{name}
%{_libdir}/%{name}
%_libdir/nautilus/extensions-2.0/libnautilus-brasero-extension.*
%{_datadir}/applications/*
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/apps/*
%{_mandir}/man1/%{name}.1*
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/omf/%{name}/*-C.omf

%files -n %libname
%defattr(-,root,root)
%_libdir/libbrasero-burn.so.%{major}*
%_libdir/libbrasero-media.so.%{major}*
%_libdir/libbrasero-utils.so.%{major}*
%_libdir/girepository-1.0/BraseroBurn-1.0.typelib
%_libdir/girepository-1.0/BraseroMedia-1.0.typelib


%files -n %develname
%defattr(-,root,root)
%_libdir/libbrasero-*.so
%_libdir/libbrasero-*.la
%_libdir/pkgconfig/*.pc
%_includedir/%name
%_datadir/gtk-doc/html/libbrasero*
%_datadir/gir-1.0/BraseroBurn-1.0.gir
%_datadir/gir-1.0/BraseroMedia-1.0.gir
