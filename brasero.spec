%define _disable_ld_no_undefined 1

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
Version: 	0.7.91
Release: 	%{release}
# For SVN: svn co http://svn.gnome.org/svn/brasero/trunk brasero
Source0:	http://ftp.gnome.org/pub/gnome/sources/brasero/0.7/%{distname}
# Fix error in .desktop file - AdamW 2008/04
Patch0:		brasero-761-desktop.patch
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
BuildRequires:	desktop-file-utils
BuildRequires:	libgstreamer0.10-plugins-base-devel
BuildRequires:	libburn-devel
BuildRequires:	libisofs-devel
BuildRequires:	libgcrypt-devel
BuildRequires:	libusb0.1-devel
BuildRequires:	gnome-doc-utils
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
%patch0 -p1 -b .desktop

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
%{_datadir}/applications/*
%{_datadir}/%{name}
%{_datadir}/icons/hicolor/*/apps/*
%{_mandir}/man1/%{name}.1*
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/omf/%{name}/*-C.omf

