%define url_ver	%(echo %{version}|cut -d. -f1,2)

%define gstapi	1.0
%define major	1
%define api	3
%define gimajor 3.1
%define libnameburn	%mklibname %{name}-burn %{api} %{major}
%define libnamemedia	%mklibname %{name}-media %{api} %{major}
%define libnameutils	%mklibname %{name}-utils %{api} %{major}
%define girmedia	%mklibname %{name}-media-gir %{gimajor}
%define girburn		%mklibname %{name}-burn-gir %{gimajor}
%define devname		%mklibname -d %{name}

Summary:	A disc burning application for GNOME
Name:		brasero
Version:	3.12.0
Release:	1
License:	GPLv2+
Group:		Archiving/Cd burning
Url:		http://www.gnome.org/projects/brasero/
Source0:	http://ftp.gnome.org/pub/GNOME/sources/brasero/%{url_ver}/%{name}-%{version}.tar.xz
Source1:	brasero_copy_disc.desktop
Source2:	brasero_create_data_project_from_blank_medium.desktop
Source3:	brasero_create_audio_cd_from_blank_medium.desktop

BuildRequires:	gnome-common
BuildRequires:	gtk-doc
BuildRequires:	glib2.0-common
BuildRequires:	imagemagick
BuildRequires:	intltool >= 0.35.0
BuildRequires:	itstool
BuildRequires:	gettext-devel
BuildRequires:	tracker-devel
BuildRequires:	yelp-tools
BuildRequires:	pkgconfig(glib-2.0) >= 2.28.0
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	pkgconfig(gobject-introspection-1.0) >= 0.6.3
BuildRequires:	pkgconfig(gstreamer-%{gstapi})
BuildRequires:	pkgconfig(gstreamer-plugins-base-%{gstapi})
BuildRequires:	pkgconfig(gthread-2.0) >= 2.6.0
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.0.0
BuildRequires:	pkgconfig(ice)
BuildRequires:	pkgconfig(libburn-1) >= 0.4.0
BuildRequires:	pkgconfig(libcanberra) >= 0.1
BuildRequires:	pkgconfig(libcanberra-gtk3) >= 0.1
BuildRequires:	pkgconfig(libisofs-1) >= 0.6.4
BuildRequires:	pkgconfig(libnautilus-extension) >= 2.91.90
BuildRequires:	pkgconfig(libnotify) >= 0.6.1
BuildRequires:	pkgconfig(libxml-2.0) >= 2.6.0
BuildRequires:	pkgconfig(sm)
BuildRequires:	pkgconfig(totem-plparser) >= 2.29.1

# optional requirements to make video projects work
Suggests:	vcdimager
Suggests:	dvdauthor
Suggests:	gstreamer%{gstapi}-plugins-bad

%description
Brasero is yet another CD / DVD writing application for the GNOME
desktop. It is designed to be as simple as possible and has some
unique features to enable users to create their discs easily and
quickly. It can handle both audio and data discs, and can use either
cdrkit or libburn / libisofs as the writing backend.

%package -n %{libnameburn}
Group:		System/Libraries
Summary:	A disc burning application for GNOME - shared library

%description -n %{libnameburn}
Brasero is yet another CD / DVD writing application for the GNOME
desktop. It is designed to be as simple as possible and has some
unique features to enable users to create their discs easily and
quickly. It can handle both audio and data discs, and can use either
cdrkit or libburn / libisofs as the writing backend.

%package -n %{libnamemedia}
Group:		System/Libraries
Summary:	A disc burning application for GNOME - shared library

%description -n %{libnamemedia}
Brasero is yet another CD / DVD writing application for the GNOME
desktop. It is designed to be as simple as possible and has some
unique features to enable users to create their discs easily and
quickly. It can handle both audio and data discs, and can use either
cdrkit or libburn / libisofs as the writing backend.

%package -n %{libnameutils}
Group:		System/Libraries
Summary:	A disc burning application for GNOME - shared library

%description -n %{libnameutils}
Brasero is yet another CD / DVD writing application for the GNOME
desktop. It is designed to be as simple as possible and has some
unique features to enable users to create their discs easily and
quickly. It can handle both audio and data discs, and can use either
cdrkit or libburn / libisofs as the writing backend.

%package -n %{girburn}
Summary:	GObject Introspection interface description for GData
Group:		System/Libraries
Requires:	%{libnameburn} = %{version}-%{release}
Obsoletes:	%{_lib}%{name}-burn-gir3.6.1 < 3.2.0-2

%description -n %{girburn}
GObject Introspection interface description for GData.

%package -n %{girmedia}
Summary:	GObject Introspection interface description for GData
Group:		System/Libraries
Requires:	%{libnamemedia} = %{version}-%{release}
Obsoletes:	%{_lib}%{name}-media-gir3.6.1 < 3.2.0-2

%description -n %{girmedia}
GObject Introspection interface description for GData.

%package -n %{devname}
Summary:	A disc burning application for GNOME - development library
Group:		Development/C
Requires:	%{libnameburn} = %{version}-%{release}
Requires:	%{libnamemedia} = %{version}-%{release}
Requires:	%{libnameutils} = %{version}-%{release}
Requires:	%{girburn} = %{version}-%{release}
Requires:	%{girmedia} = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}

%description -n %{devname}
Brasero is yet another CD / DVD writing application for the GNOME
desktop. It is designed to be as simple as possible and has some
unique features to enable users to create their discs easily and
quickly. It can handle both audio and data discs, and can use either
cdrkit or libburn / libisofs as the writing backend.

%prep
%setup -q
%apply_patches

%build
%configure \
        --enable-nautilus \
        --enable-libburnia \
        --enable-search \
        --enable-playlist \
        --enable-preview \
        --enable-inotify \
        --disable-caches \
	--enable-compile-warnings=no

%make 

%install
%makeinstall_std

sed -i 's/cd:x/cd;x/' %{buildroot}%{_datadir}/applications/%{name}.desktop

%find_lang %{name} --with-gnome

#(nl) KDE Solid integration
mkdir -p %{buildroot}%{_datadir}/apps/solid/actions
install -D -m 644 %{SOURCE1} %{buildroot}%{_datadir}/apps/solid/actions/
install -D -m 644 %{SOURCE2} %{buildroot}%{_datadir}/apps/solid/actions/
install -D -m 644 %{SOURCE3} %{buildroot}%{_datadir}/apps/solid/actions/

%files -f %{name}.lang
%doc AUTHORS MAINTAINERS NEWS README
%{_bindir}/%{name}
%{_libdir}/%{name}%{api}
%{_libdir}/nautilus/extensions-3.0/libnautilus-brasero-extension.*
%{_datadir}/applications/*
%{_datadir}/appdata/*
%{_datadir}/%{name}
%{_datadir}/apps/solid/actions/*
%{_datadir}/glib-2.0/schemas/org.gnome.brasero.gschema.xml
%{_datadir}/GConf/gsettings/brasero.convert
%{_datadir}/mime/packages/%{name}.xml
%{_iconsdir}/hicolor/*/apps/*
%{_mandir}/man1/%{name}.1*

%files -n %{libnameburn}
%{_libdir}/lib%{name}-burn%{api}.so.%{major}*

%files -n %{libnamemedia}
%{_libdir}/lib%{name}-media%{api}.so.%{major}*

%files -n %{libnameutils}
%{_libdir}/lib%{name}-utils%{api}.so.%{major}*

%files -n %{girburn}
%{_libdir}/girepository-1.0/BraseroBurn-%{gimajor}.typelib

%files -n %{girmedia}
%{_libdir}/girepository-1.0/BraseroMedia-%{gimajor}.typelib

%files -n %devname
%doc %{_datadir}/gtk-doc/html/libbrasero*
%{_libdir}/lib%{name}-*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/%{name}%{api}
%{_datadir}/gir-1.0/BraseroBurn-%{gimajor}.gir
%{_datadir}/gir-1.0/BraseroMedia-%{gimajor}.gir

