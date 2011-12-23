%define distname	%{name}-%{version}.tar.bz2
%define dir_name	%{name}-%{version}

%define major 1
%define libname %mklibname %{name} %major
%define develname %mklibname -d %{name}

Name: 	 	brasero
Summary: 	A disc burning application for GNOME
Version: 	2.32.1
Release: 	7
Source0:	http://ftp.gnome.org/pub/GNOME/sources/brasero/%{distname}
Source1:    brasero_copy_disc.desktop
Source2:    brasero_create_data_project_from_blank_medium.desktop
Source3:    brasero_create_audio_cd_from_blank_medium.desktop
Patch0:		brasero-2.32.1-fix-zh_CN.patch
URL:		http://www.gnome.org/projects/brasero/
License:	GPLv2+
Group:		Archiving/Cd burning

BuildRequires:	imagemagick
BuildRequires:	libgstreamer-devel >= 0.10.15
BuildRequires:	libxml2-devel >= 2.6.0
BuildRequires:	nautilus-devel >= 2.22.2
BuildRequires:	tracker-devel >= 0.7.0
BuildRequires:	libGConf2-devel
BuildRequires:	totem-plparser-devel >= 2.22.0
BuildRequires:	pkgconfig(gdl-1.0)
BuildRequires:	dbus-glib-devel >= 0.7.2
BuildRequires:	libgstreamer0.10-plugins-base-devel >= 0.10.0
BuildRequires:	unique-devel
BuildRequires:	libcanberra-gtk-devel
BuildRequires:	gobject-introspection-devel
BuildRequires:	gnome-doc-utils
BuildRequires:	gtk-doc >= 1.12
BuildRequires:	intltool >= 0.35.0
BuildRequires:	gnome-common
BuildRequires:	libsm-devel

Requires(post): desktop-file-utils
Requires(postun): desktop-file-utils
Requires:	cdrkit
Suggests:	cdrdao
Suggests:	dvd+rw-tools

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

%package -n %{libname}
Group: System/Libraries
Summary: A disc burning application for GNOME - shared library

%description -n %{libname}
Brasero is yet another CD / DVD writing application for the GNOME
desktop. It is designed to be as simple as possible and has some
unique features to enable users to create their discs easily and
quickly. It can handle both audio and data discs, and can use either
cdrkit or libburn / libisofs as the writing backend.

%package -n %{develname}
Summary: A disc burning application for GNOME - development library
Group: Development/C
Requires: %{libname} = %{version}-%{release}
Provides: %{name}-devel = %{version}-%{release}

%description -n %{develname}
Brasero is yet another CD / DVD writing application for the GNOME
desktop. It is designed to be as simple as possible and has some
unique features to enable users to create their discs easily and
quickly. It can handle both audio and data discs, and can use either
cdrkit or libburn / libisofs as the writing backend.

%prep
%setup -q
%apply_patches

%build
# libburn backend disabled for now (0.8.1 2008/08), it's not working;
# will restore when upstream advises it - AdamW
%configure2_5x \
	--disable-static \
	--disable-schemas-install \
	--disable-caches \
   	--enable-search=tracker \
   	--enable-libburnia=no \
	--enable-gtk3=no
%make 

%install
rm -rf %{buildroot}
%makeinstall_std

%find_lang %{name} --with-gnome

for omf in %{buildroot}%{_datadir}/omf/%{name}/%{name}-??*.omf;do 
echo "%lang($(basename $omf|sed -e s/brasero-// -e s/.omf//)) $(echo $omf|sed -e s!%{buildroot}!!)" >> %{name}.lang
done

#(nl) KDE Solid integration
mkdir -p %{buildroot}/%{_datadir}/apps/solid/actions
install -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/apps/solid/actions/
install -D -m 644 %{SOURCE2} %{buildroot}%{_datadir}/apps/solid/actions/
install -D -m 644 %{SOURCE3} %{buildroot}%{_datadir}/apps/solid/actions/

%files -f %{name}.lang
%doc AUTHORS MAINTAINERS NEWS README
%{_bindir}/%{name}
%{_libdir}/%{name}
%{_libdir}/nautilus/extensions-2.0/libnautilus-brasero-extension.*
%{_datadir}/applications/*
%{_datadir}/%{name}
%{_datadir}/glib-2.0/schemas/org.gnome.brasero.gschema.xml
%{_datadir}/GConf/gsettings/brasero.convert
%{_datadir}/icons/hicolor/*/apps/*
%{_mandir}/man1/%{name}.1*
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/omf/%{name}/*-C.omf
%{_datadir}/apps/solid/actions/

%files -n %{libname}
%{_libdir}/libbrasero-burn.so.%{major}*
%{_libdir}/libbrasero-media.so.%{major}*
%{_libdir}/libbrasero-utils.so.%{major}*
%{_libdir}/girepository-1.0/BraseroBurn-%{version}.typelib
%{_libdir}/girepository-1.0/BraseroMedia-%{version}.typelib


%files -n %{develname}
%{_libdir}/libbrasero-*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/%{name}
%{_datadir}/gtk-doc/html/libbrasero*
%{_datadir}/gir-1.0/BraseroBurn-%{version}.gir
%{_datadir}/gir-1.0/BraseroMedia-%{version}.gir
