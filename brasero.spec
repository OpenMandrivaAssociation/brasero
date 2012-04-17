%define major		1
%define api		3
%define gi_major	%{version}

%define libnameburn3	%mklibname %{name}-burn %{api} %{major}
%define libnamemedia3	%mklibname %{name}-media %{api} %{major}
%define libnameutils3	%mklibname %{name}-utils %{api} %{major}

%define girmedia	%mklibname %{name}-media-gir %{gi_major}
%define girburn		%mklibname %{name}-burn-gir %{gi_major}

%define develname	%mklibname -d %{name}

%define url_ver	%(echo %{version}|cut -d. -f1,2)

Name: 	 	brasero
Summary: 	A disc burning application for GNOME
Version: 	3.4.1
Release: 	%mkrel 1
Source0:	http://download.gnome.org/sources/%{name}/%{url_ver}/%{name}-%{version}.tar.xz
Source1:	brasero_copy_disc.desktop
Source2:	brasero_create_data_project_from_blank_medium.desktop
Source3:	brasero_create_audio_cd_from_blank_medium.desktop
Patch2:		brasero-3.2.0-linkage.patch
URL:		http://www.gnome.org/projects/brasero/
License:	GPLv2+
Group:		Archiving/Cd burning
BuildRequires:	pkgconfig(gdk-x11-3.0)
BuildRequires:	pkgconfig(glib-2.0) >= 2.28.0
BuildRequires:	pkgconfig(gmodule-2.0) >= 2.6.0
BuildRequires:	pkgconfig(gmodule-export-2.0) >= 2.6.0
BuildRequires:	pkgconfig(gobject-2.0) >= 2.28.0
BuildRequires:	pkgconfig(gobject-introspection-1.0) >= 0.6.3
BuildRequires:	pkgconfig(gio-2.0) >= 2.28.0
BuildRequires:	pkgconfig(gstreamer-0.10) >= 0.10.15
BuildRequires:	pkgconfig(gstreamer-interfaces-0.10)
BuildRequires:	pkgconfig(gstreamer-plugins-base-0.10) >= 0.10.0
BuildRequires:	pkgconfig(gthread-2.0) >= 2.6.0
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.0.0
BuildRequires:	pkgconfig(ice)
BuildRequires:	tracker-devel
BuildRequires:	pkgconfig(libburn-1) >= 0.4.0
BuildRequires:	pkgconfig(libcanberra) >= 0.1
BuildRequires:	pkgconfig(libcanberra-gtk3) >= 0.1
BuildRequires:	pkgconfig(libisofs-1) >= 0.6.4
BuildRequires:	pkgconfig(libnautilus-extension) >= 2.91.90
BuildRequires:	pkgconfig(libnotify) >= 0.6.1
BuildRequires:	pkgconfig(libxml-2.0) >= 2.6.0
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(totem-plparser) >= 2.29.1
BuildRequires:	intltool >= 0.35.0
BuildRequires:	gnome-doc-utils
BuildRequires:	imagemagick
# Only needed when gnome-autogen.sh is used
BuildRequires:	gnome-common
BuildRequires:	gtk-doc
BuildRequires:	gettext-devel

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

%package -n %{libnameburn3}
Group:		System/Libraries
Summary:	A disc burning application for GNOME - shared library

%description -n %{libnameburn3}
Brasero is yet another CD / DVD writing application for the GNOME
desktop. It is designed to be as simple as possible and has some
unique features to enable users to create their discs easily and
quickly. It can handle both audio and data discs, and can use either
cdrkit or libburn / libisofs as the writing backend.

%package -n %{libnamemedia3}
Group:		System/Libraries
Summary:	A disc burning application for GNOME - shared library

%description -n %{libnamemedia3}
Brasero is yet another CD / DVD writing application for the GNOME
desktop. It is designed to be as simple as possible and has some
unique features to enable users to create their discs easily and
quickly. It can handle both audio and data discs, and can use either
cdrkit or libburn / libisofs as the writing backend.

%package -n %{libnameutils3}
Group:		System/Libraries
Summary:	A disc burning application for GNOME - shared library

%description -n %{libnameutils3}
Brasero is yet another CD / DVD writing application for the GNOME
desktop. It is designed to be as simple as possible and has some
unique features to enable users to create their discs easily and
quickly. It can handle both audio and data discs, and can use either
cdrkit or libburn / libisofs as the writing backend.

%package -n %{girburn}
Summary:        GObject Introspection interface description for GData
Group:          System/Libraries
Requires:       %{libnameburn3} = %{version}-%{release}
Obsoletes:	%{_lib}%{name}-burn-gir0.0 < 3.2.0-2

%description -n %{girburn}
GObject Introspection interface description for GData.

%package -n %{girmedia}
Summary:        GObject Introspection interface description for GData
Group:          System/Libraries
Requires:       %{libnamemedia3} = %{version}-%{release}
Obsoletes:	%{_lib}%{name}-media-gir0.0 < 3.2.0-2

%description -n %{girmedia}
GObject Introspection interface description for GData.

%package -n %{develname}
Summary:	A disc burning application for GNOME - development library
Group:		Development/C
Requires:	%{libnameburn3} = %{version}-%{release}
Requires:	%{libnamemedia3} = %{version}-%{release}
Requires:	%{libnameutils3} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Provides:	lib%{name}-devel = %{version}-%{release}

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
NOCONFIGURE=1 gnome-autogen.sh
%configure2_5x \
        --enable-nautilus \
        --enable-libburnia \
        --enable-search \
        --enable-playlist \
        --enable-preview \
        --enable-inotify \
        --disable-caches \
        --disable-static

%make 

%install
rm -rf %{buildroot}
%makeinstall_std

sed -i 's/cd:x/cd;x/' %{buildroot}%{_datadir}/applications/%{name}.desktop

#we don't want these
find %{buildroot} -name "*.la" -delete

%find_lang %{name} --with-gnome

#(nl) KDE Solid integration
mkdir -p %{buildroot}%{_datadir}/apps/solid/actions
install -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/apps/solid/actions/
install -D -m 644 %{SOURCE2} %{buildroot}%{_datadir}/apps/solid/actions/
install -D -m 644 %{SOURCE3} %{buildroot}%{_datadir}/apps/solid/actions/

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS MAINTAINERS NEWS README
%{_bindir}/%{name}
%{_libdir}/%{name}3
%{_libdir}/nautilus/extensions-3.0/libnautilus-brasero-extension.*
%{_datadir}/applications/*
%{_datadir}/%{name}
%{_datadir}/glib-2.0/schemas/org.gnome.brasero.gschema.xml
%{_datadir}/GConf/gsettings/brasero.convert
%{_datadir}/icons/hicolor/*/apps/*
%{_mandir}/man1/%{name}.1*
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/apps/solid/actions/*

%files -n %{libnameburn3}
%defattr(-,root,root)
%{_libdir}/lib%{name}-burn3.so.%{major}*

%files -n %{libnamemedia3}
%defattr(-,root,root)
%{_libdir}/lib%{name}-media3.so.%{major}*

%files -n %{libnameutils3}
%defattr(-,root,root)
%{_libdir}/lib%{name}-utils3.so.%{major}*

%files -n %{girburn}
%defattr(-,root,root)
%{_libdir}/girepository-1.0/BraseroBurn-%{gi_major}.typelib

%files -n %{girmedia}
%defattr(-,root,root)
%{_libdir}/girepository-1.0/BraseroMedia-%{gi_major}.typelib

%files -n %develname
%defattr(-,root,root)
%doc %{_datadir}/gtk-doc/html/libbrasero*
%{_libdir}/lib%{name}-*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/%{name}3
%{_datadir}/gir-1.0/BraseroBurn-%{gi_major}.gir
%{_datadir}/gir-1.0/BraseroMedia-%{gi_major}.gir

