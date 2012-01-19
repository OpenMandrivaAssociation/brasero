%define api 3
%define major 1
%define gir_major 3.2.0

%define libburn %mklibname %{name}-burn %{api} %{major}
%define libmedia %mklibname %{name}-media %{api} %{major}
%define libutils %mklibname %{name}-utils %{api} %{major}
%define girburn %mklibname %{name}-burn-gir %{gir_major}
%define girmedia %mklibname %{name}-media-gir %{gir_major}
%define develname %mklibname -d %{name}

Name: 	 	brasero
Summary: 	A disc burning application for GNOME
Version: 	3.2.0
Release: 	1
License:	GPLv2+
Group:		Archiving/Cd burning
URL:		http://www.gnome.org/projects/brasero/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/brasero/%{name}-%{version}.tar.xz
Source1:    brasero_copy_disc.desktop
Source2:    brasero_create_data_project_from_blank_medium.desktop
Source3:    brasero_create_audio_cd_from_blank_medium.desktop
Patch0:		brasero-3.1.90-fix-str-fmt.patch

BuildRequires:  intltool >= 0.35.0
BuildRequires:  gnome-doc-utils
BuildRequires:  imagemagick
BuildRequires:  pkgconfig(gdk-x11-3.0)
BuildRequires:  pkgconfig(glib-2.0) >= 2.28.0
BuildRequires:  pkgconfig(gmodule-2.0) >= 2.6.0
BuildRequires:  pkgconfig(gmodule-export-2.0) >= 2.6.0
BuildRequires:  pkgconfig(gobject-2.0) >= 2.28.0
BuildRequires:  pkgconfig(gobject-introspection-1.0) >= 0.6.3
BuildRequires:  pkgconfig(gio-2.0) >= 2.28.0
BuildRequires:  pkgconfig(gstreamer-0.10) >= 0.10.15
BuildRequires:  pkgconfig(gstreamer-interfaces-0.10)
BuildRequires:  pkgconfig(gstreamer-plugins-base-0.10) >= 0.10.0
BuildRequires:  pkgconfig(gthread-2.0) >= 2.6.0
BuildRequires:  pkgconfig(gtk+-3.0) >= 3.0.0
BuildRequires:  pkgconfig(ice)
BuildRequires:  pkgconfig(libburn-1) >= 0.4.0
BuildRequires:  pkgconfig(libcanberra) >= 0.1
BuildRequires:  pkgconfig(libcanberra-gtk3) >= 0.1
BuildRequires:  pkgconfig(libisofs-1) >= 0.6.4
BuildRequires:  pkgconfig(libnautilus-extension) >= 2.91.90
BuildRequires:  pkgconfig(libnotify) >= 0.6.1
BuildRequires:  pkgconfig(libxml-2.0) >= 2.6.0
BuildRequires:  pkgconfig(sm)
BuildRequires:  pkgconfig(totem-plparser) >= 2.29.1
BuildRequires:  pkgconfig(tracker-sparql-0.12)

Suggests:	cdrkit
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

%package -n %{libburn}
Group: System/Libraries
Summary: A disc burning application for GNOME - shared library

%description -n %{libburn}
This package contains the shared library libburn for %{name}.

%package -n %{libmedia}
Group: System/Libraries
Summary: A disc burning application for GNOME - shared library

%description -n %{libmedia}
This package contains the shared library libburn for %{name}.

%package -n %{libutils}
Group: System/Libraries
Summary: A disc burning application for GNOME - shared library

%description -n %{libutils}
This package contains the shared library libburn for %{name}.

%package -n %{girburn}
Summary: GObject Introspection interface description for %{name}
Group: System/Libraries
Requires: %{libburn} = %{version}-%{release}

%description -n %{girburn}
GObject Introspection interface description for %{name}.

%package -n %{girmedia}
Summary: GObject Introspection interface description for %{name}
Group: System/Libraries
Requires: %{libburn} = %{version}-%{release}

%description -n %{girmedia}
GObject Introspection interface description for %{name}.

%package -n %{develname}
Summary: A disc burning application for GNOME - development library
Group: Development/C
Requires: %{libburn} = %{version}-%{release}
Requires: %{libmedia} = %{version}-%{release}
Requires: %{libutils} = %{version}-%{release}
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
%configure2_5x \
	--disable-static \
	--disable-caches \
   	--enable-search \
   	--enable-libburnia \
	--enable-playlist \
	--enable-preview \
	--enable-inotify \
	--enable-nautilus

%make LIBS='-lm'

%install
rm -rf %{buildroot}
%makeinstall_std
find %{buildroot} -name "*.la" -delete

%find_lang %{name} --with-gnome


#(nl) KDE Solid integration
mkdir -p %{buildroot}/%{_datadir}/apps/solid/actions
install -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/apps/solid/actions/
install -D -m 644 %{SOURCE2} %{buildroot}%{_datadir}/apps/solid/actions/
install -D -m 644 %{SOURCE3} %{buildroot}%{_datadir}/apps/solid/actions/

%files -f %{name}.lang
%doc AUTHORS MAINTAINERS NEWS README
%{_bindir}/%{name}
%{_libdir}/%{name}%{api}
%{_libdir}/nautilus/extensions-3.0/libnautilus-brasero-extension.*
%{_datadir}/applications/*
%{_datadir}/%{name}
%{_datadir}/glib-2.0/schemas/org.gnome.brasero.gschema.xml
%{_datadir}/GConf/gsettings/brasero.convert
%{_datadir}/icons/hicolor/*/apps/*
%{_mandir}/man1/%{name}.1*
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/apps/solid/actions/

%files -n %{libburn}
%{_libdir}/libbrasero-burn%{api}.so.%{major}*

%files -n %{libmedia}
%{_libdir}/libbrasero-media%{api}.so.%{major}*

%files -n %{libutils}
%{_libdir}/libbrasero-utils%{api}.so.%{major}*

%files -n %{girburn}
%{_libdir}/girepository-1.0/BraseroBurn-%{gir_major}.typelib

%files -n %{girmedia}
%{_libdir}/girepository-1.0/BraseroMedia-%{gir_major}.typelib

%files -n %{develname}
%{_libdir}/libbrasero-*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/%{name}
%{_datadir}/gtk-doc/html/libbrasero*
%{_datadir}/gir-1.0/BraseroBurn-%{gir_major}.gir
%{_datadir}/gir-1.0/BraseroMedia-%{gir_major}.gir
