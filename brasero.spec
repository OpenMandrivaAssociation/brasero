%define svn	0
%define rel	1
%if %svn
%define release		%mkrel 0.%svn.%rel
%define distname	%name-%svn.tar.lzma
%define dirname		%name
%else
%define release		%mkrel %rel
%define distname	%name-%version.tar.bz2
%define dirname		%name-%version
%endif

Name: 	 	brasero
Summary: 	A disc burning application for GNOME
Version: 	0.9.0
Release: 	%{release}
# For SVN: svn co http://svn.gnome.org/svn/brasero/trunk brasero
Source0:	http://ftp.gnome.org/pub/gnome/sources/brasero/0.9/%{distname}
Patch0:		brasero-0.9.0-format-strings.patch
Patch1:		brasero-0.9.0-fix-linkage.patch
Patch2:		brasero-0.9.0-link-gobject.patch
URL:		http://www.gnome.org/projects/brasero/
License:	GPLv2+
Group:		Archiving/Cd burning
BuildRoot:	%{_tmppath}/%{name}-buildroot
BuildRequires:	imagemagick
BuildRequires:	libgnome-vfs2-devel
BuildRequires:	libgnomeui2-devel
BuildRequires:	libgnome2-devel
BuildRequires:	libgstreamer-devel >= 0.10
BuildRequires:	libxml2-devel
BuildRequires:	nautilus-devel eel-devel
BuildRequires:	hal-devel
BuildRequires:	libbeagle-devel >= 0.2.5
BuildRequires:	totem-plparser-devel
BuildRequires:	libgdl-devel >= 0.6
BuildRequires:	libgstreamer0.10-plugins-base-devel
#BuildRequires:	libburn-devel
#BuildRequires:	libisofs-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	libusb0.1-devel
BuildRequires:	gnome-doc-utils
BuildRequires:	gtk-doc
BuildRequires:	intltool
%if %svn
BuildRequires:	autoconf
BuildRequires:	gnome-common
%endif
Requires:	hal >= 0.5.0

Obsoletes:	bonfire
Provides:	bonfire

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

%prep
%setup -q -n %{dirname}
%patch0 -p1 -b .format-strings
%patch1 -p0 -b .linkage
%patch2 -p0 -b .lgobject

%build
%if %svn
./autogen.sh
%endif
autoreconf
# libburn backend disabled for now (0.8.1 2008/08), it's not working;
# will restore when upstream advises it - AdamW
%configure2_5x --disable-schemas-install \
               --disable-caches \
               --enable-libburnia=no \
               --enable-gtk-doc
%make

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

