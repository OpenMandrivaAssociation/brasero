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

Name:		brasero
Summary:	A disc burning application for GNOME
Version:	3.6.1
Release:	1
Source0:	ftp://ftp.gnome.org/pub/GNOME/sources//%{name}/%{url_ver}/%{name}-%{version}.tar.xz
Source1:	brasero_copy_disc.desktop
Source2:	brasero_create_data_project_from_blank_medium.desktop
Source3:	brasero_create_audio_cd_from_blank_medium.desktop
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
BuildRequires:	pkgconfig(gstreamer-1.0)
BuildRequires:	pkgconfig(gstreamer-plugins-base-1.0)
BuildRequires:	pkgconfig(gthread-2.0) >= 2.6.0
BuildRequires:	pkgconfig(gtk+-3.0) >= 3.0.0
BuildRequires:	pkgconfig(ice)
BuildRequires:	tracker-devel glib2.0-common
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
BuildRequires:	pkgconfig(gnome-doc-utils)
BuildRequires:	imagemagick
# Only needed when gnome-autogen.sh is used
BuildRequires:	gnome-common
BuildRequires:	gtk-doc
BuildRequires:	gettext-devel itstool

# optional requirements to make video projects work
Suggests:	vcdimager
Suggests:	dvdauthor
Suggests:	gstreamer1.0-plugins-bad

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
Summary:	GObject Introspection interface description for GData
Group:		System/Libraries
Requires:	%{libnameburn3} = %{version}-%{release}
Obsoletes:	%{_lib}%{name}-burn-gir0.0 < 3.2.0-2

%description -n %{girburn}
GObject Introspection interface description for GData.

%package -n %{girmedia}
Summary:	GObject Introspection interface description for GData
Group:		System/Libraries
Requires:	%{libnamemedia3} = %{version}-%{release}
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

%files -f %{name}.lang
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
%{_libdir}/lib%{name}-burn3.so.%{major}*

%files -n %{libnamemedia3}
%{_libdir}/lib%{name}-media3.so.%{major}*

%files -n %{libnameutils3}
%{_libdir}/lib%{name}-utils3.so.%{major}*

%files -n %{girburn}
%{_libdir}/girepository-1.0/BraseroBurn-3.6.0.typelib

%files -n %{girmedia}
%{_libdir}/girepository-1.0/BraseroMedia-3.6.0.typelib

%files -n %develname
%doc %{_datadir}/gtk-doc/html/libbrasero*
%{_libdir}/lib%{name}-*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/%{name}3
%{_datadir}/gir-1.0/BraseroBurn-3.6.0.gir
%{_datadir}/gir-1.0/BraseroMedia-3.6.0.gir



%changelog
* Fri Dec  7 2012 Arkady L. Shane <ashejn@rosalab.ru> 3.6.1-1
- update to 3.6.1

* Tue Oct  9 2012 Arkady L. Shane <ashejn@rosalab.ru> 3.6.0-1
- update to 3.6.0

* Tue Apr 17 2012 Alexander Khrukin <akhrukin@mandriva.org> 3.4.1-1mdv2012.0
+ Revision: 791439
- BR:tracker-devel
- version update 3.4.1

* Thu Jan 19 2012 Matthew Dawkins <mattydaw@mandriva.org> 3.2.0-1
+ Revision: 762796
- added missing BR glib2.0-common
- fixed files list for includes
- actually add p0
- fixed lib naming
- added p0 (thx mga)
- new version 3.2.0
- cleaned up spec
- converted BRs to pkgconfig provides
- split out gir and lib pkgs
- employed new api and gir major
- attempt to link properly against libm
- more clean ups
- fixed BR name
- bump release
- rebuild
- cleaned up spec
- prep for major upgrade

* Sun Oct 16 2011 Götz Waschk <waschk@mandriva.org> 2.32.1-6
+ Revision: 704892
- rebuild for gmime

* Sat Sep 03 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 2.32.1-5
+ Revision: 698154
- rebuild for new libburn

* Mon May 09 2011 Funda Wang <fwang@mandriva.org> 2.32.1-4
+ Revision: 673046
- fix a nasty translation bug reported by ubuntu community

* Sun Apr 10 2011 Funda Wang <fwang@mandriva.org> 2.32.1-3
+ Revision: 652195
- rebuild

  + Matthew Dawkins <mattydaw@mandriva.org>
    - added missing BR
    - added missing requires for cdrkit
    - added suggests for cdrdao and dvd+rw-tools
    - changed dirname macro to dir_name for rpm5
    - eliminated extra macro rel just to set mkrel macro

* Mon Nov 15 2010 Götz Waschk <waschk@mandriva.org> 2.32.1-1mdv2011.0
+ Revision: 597760
- update to new version 2.32.1

  + John Balcaen <mikala@mandriva.org>
    - Fix BR for libcanberra-gtk-devel

* Mon Sep 27 2010 Götz Waschk <waschk@mandriva.org> 2.32.0-1mdv2011.0
+ Revision: 581463
- update to new version 2.32.0

* Tue Sep 14 2010 Götz Waschk <waschk@mandriva.org> 2.31.92-1mdv2011.0
+ Revision: 578316
- new version

* Tue Aug 31 2010 Götz Waschk <waschk@mandriva.org> 2.31.91-1mdv2011.0
+ Revision: 574572
- update to new version 2.31.91

* Wed Aug 18 2010 Götz Waschk <waschk@mandriva.org> 2.31.90-1mdv2011.0
+ Revision: 571172
- new version
- drop patch
- new major
- update file list, replace gconf by gsettings

* Sat Jul 31 2010 Funda Wang <fwang@mandriva.org> 2.30.2-2mdv2011.0
+ Revision: 563901
- rebuild for new gobject-introspection

* Tue Jun 22 2010 Frederic Crozat <fcrozat@mandriva.com> 2.30.2-1mdv2010.1
+ Revision: 548524
- Release 2.30.2
- Remove patch1 (merged upstream)

* Fri May 14 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 2.30.1-5mdv2010.1
+ Revision: 544744
- Update solid action translations

* Tue May 11 2010 Luis Medinas <lmedinas@mandriva.org> 2.30.1-4mdv2010.1
+ Revision: 544489
- Added patch from upstream git to fix tracker search and memleaks

* Mon May 10 2010 Nicolas Lécureuil <nlecureuil@mandriva.com> 2.30.1-3mdv2010.1
+ Revision: 544372
- Add KDE Solid actions

* Wed Apr 28 2010 Christophe Fergeau <cfergeau@mandriva.com> 2.30.1-2mdv2010.1
+ Revision: 540333
- rebuild so that shared libraries are properly stripped again

* Tue Apr 27 2010 Götz Waschk <waschk@mandriva.org> 2.30.1-1mdv2010.1
+ Revision: 539481
- new version
- drop patch 1

* Mon Apr 26 2010 Frederic Crozat <fcrozat@mandriva.com> 2.30.0-2mdv2010.1
+ Revision: 538957
- Fix buildrequires for x86-67
- Patch1: fix build with tracker 0.8.x (GNOME bug #616831)

* Mon Mar 29 2010 Götz Waschk <waschk@mandriva.org> 2.30.0-1mdv2010.1
+ Revision: 528912
- new version
- drop patch 1

* Mon Mar 15 2010 Götz Waschk <waschk@mandriva.org> 2.29.92-2mdv2010.1
+ Revision: 519133
- don't hang on startup (b.g.o #611111)

* Fri Mar 12 2010 Götz Waschk <waschk@mandriva.org> 2.29.92-1mdv2010.1
+ Revision: 518304
- update to new version 2.29.92

* Mon Feb 22 2010 Götz Waschk <waschk@mandriva.org> 2.29.91-1mdv2010.1
+ Revision: 509814
- update to new version 2.29.91

* Tue Feb 09 2010 Götz Waschk <waschk@mandriva.org> 2.29.90-1mdv2010.1
+ Revision: 502598
- update to new version 2.29.90

* Wed Jan 27 2010 Götz Waschk <waschk@mandriva.org> 2.29.6-1mdv2010.1
+ Revision: 496951
- update to new version 2.29.6

* Tue Dec 22 2009 Götz Waschk <waschk@mandriva.org> 2.29.4-1mdv2010.1
+ Revision: 481619
- update to new version 2.29.4

* Sat Dec 19 2009 Götz Waschk <waschk@mandriva.org> 2.29.3-1mdv2010.1
+ Revision: 480184
- new version
- update deps
- rediff patch
- update file list

* Mon Dec 14 2009 Götz Waschk <waschk@mandriva.org> 2.28.3-1mdv2010.1
+ Revision: 478639
- update to new version 2.28.3

* Wed Oct 21 2009 Frederic Crozat <fcrozat@mandriva.com> 2.28.2-1mdv2010.0
+ Revision: 458621
- Release 2.28.2

* Mon Oct 05 2009 Götz Waschk <waschk@mandriva.org> 2.28.1-1mdv2010.0
+ Revision: 454158
- update to new version 2.28.1

* Mon Sep 21 2009 Götz Waschk <waschk@mandriva.org> 2.28.0-1mdv2010.0
+ Revision: 446622
- update to new version 2.28.0

* Thu Sep 10 2009 Götz Waschk <waschk@mandriva.org> 2.27.92-1mdv2010.0
+ Revision: 437413
- update to new version 2.27.92

* Wed Aug 26 2009 Götz Waschk <waschk@mandriva.org> 2.27.91-1mdv2010.0
+ Revision: 421333
- update to new version 2.27.91

* Mon Aug 10 2009 Götz Waschk <waschk@mandriva.org> 2.27.90-1mdv2010.0
+ Revision: 414459
- new version
- update file list

* Mon Jul 27 2009 Götz Waschk <waschk@mandriva.org> 2.27.5-2mdv2010.0
+ Revision: 400789
- update build deps
- new version
- drop patch 1

* Wed Jul 15 2009 Götz Waschk <waschk@mandriva.org> 2.27.4-2mdv2010.0
+ Revision: 396190
- fix pkgconfig file

* Tue Jul 14 2009 Götz Waschk <waschk@mandriva.org> 2.27.4-1mdv2010.0
+ Revision: 395775
- new version
- update deps
- rediff the patch

* Tue Jun 16 2009 Götz Waschk <waschk@mandriva.org> 2.27.3-1mdv2010.0
+ Revision: 386288
- new version
- fix format strings

* Tue May 26 2009 Götz Waschk <waschk@mandriva.org> 2.27.2-1mdv2010.0
+ Revision: 379962
- update to new version 2.27.2

* Mon May 11 2009 Götz Waschk <waschk@mandriva.org> 2.27.1-1mdv2010.0
+ Revision: 374298
- update build deps
- new version
- fix build
- update file list

* Tue Apr 14 2009 Götz Waschk <waschk@mandriva.org> 2.26.1-1mdv2009.1
+ Revision: 367221
- new version
- drop patch

* Tue Apr 07 2009 Frederic Crozat <fcrozat@mandriva.com> 2.26.0-3mdv2009.1
+ Revision: 364847
- Update patch0 with more crash fixes from SVN

* Mon Apr 06 2009 Frederic Crozat <fcrozat@mandriva.com> 2.26.0-2mdv2009.1
+ Revision: 364362
- Patch0 (SVN): many crash fixes from SVN

* Mon Mar 16 2009 Götz Waschk <waschk@mandriva.org> 2.26.0-1mdv2009.1
+ Revision: 355629
- update to new version 2.26.0
- obsolete nautilus-cd-burner

* Mon Mar 02 2009 Götz Waschk <waschk@mandriva.org> 2.25.92-1mdv2009.1
+ Revision: 346876
- update to new version 2.25.92

* Tue Feb 17 2009 Götz Waschk <waschk@mandriva.org> 2.25.91.2-1mdv2009.1
+ Revision: 342176
- new version

* Tue Feb 17 2009 Götz Waschk <waschk@mandriva.org> 2.25.91.1-1mdv2009.1
+ Revision: 341479
- new version

* Tue Feb 17 2009 Götz Waschk <waschk@mandriva.org> 2.25.91-1mdv2009.1
+ Revision: 341434
- new version
- drop patches

* Sun Feb 01 2009 Funda Wang <fwang@mandriva.org> 2.25.90-2mdv2009.1
+ Revision: 336214
- more linkage fix

* Sun Feb 01 2009 Funda Wang <fwang@mandriva.org> 2.25.90-1mdv2009.1
+ Revision: 336200
- fix linkage with gst
- New version 2.25.90

  + Götz Waschk <waschk@mandriva.org>
    - fix source URL

* Mon Jan 19 2009 Götz Waschk <waschk@mandriva.org> 0.9.1-1mdv2009.1
+ Revision: 331326
- new version
- drop all patches
- add library package

* Tue Jan 06 2009 Funda Wang <fwang@mandriva.org> 0.9.0-1mdv2009.1
+ Revision: 325191
- use gnome-autogen
- let plugins link with gobject
- New versino 0.9.0
- fix linkage rather than disable lflags
- rediff format patch

* Fri Dec 19 2008 Götz Waschk <waschk@mandriva.org> 0.8.4-1mdv2009.1
+ Revision: 316152
- new version
- fix build
- update build deps
- add nautilus extensions

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Tue Nov 11 2008 Frederik Himpe <fhimpe@mandriva.org> 0.8.3-1mdv2009.1
+ Revision: 302117
- Update to new version 0.8.3

* Tue Sep 23 2008 Frederik Himpe <fhimpe@mandriva.org> 0.8.2-1mdv2009.0
+ Revision: 287600
- Suggest optional requirements to make video projects work
- Add BuildRequires to fix build of the help
- Update to new version 0.8.2 (important bug fixes)

* Mon Aug 25 2008 Adam Williamson <awilliamson@mandriva.org> 0.8.1-2mdv2009.0
+ Revision: 275968
- disable libburn backend, it's not working

* Sat Aug 09 2008 Funda Wang <fwang@mandriva.org> 0.8.1-1mdv2009.0
+ Revision: 270118
- New version 0.8.1

* Mon Jul 14 2008 Adam Williamson <awilliamson@mandriva.org> 0.8.0-1mdv2009.0
+ Revision: 234448
- drop now unnecessary buildrequires
- drop menu patch and workaround (fixed upstream)
- new version 0.8.0

* Thu Jul 03 2008 Adam Williamson <awilliamson@mandriva.org> 0.7.91-1mdv2009.0
+ Revision: 231372
- drop build.patch (merged upstream)
- new release 0.7.91

* Sat Jun 28 2008 Adam Williamson <awilliamson@mandriva.org> 0.7.90-1mdv2009.0
+ Revision: 229597
- crib a little loop from eog to handle omf files by language
- use --with-gnome for find-lang
- add build.patch: fixes build for GCC 4.3 (from upstream SVN)
- disable underlinking protection (only plugins, no shared libs)
- small spec clean
- new release 0.7.90

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

* Wed May 14 2008 Adam Williamson <awilliamson@mandriva.org> 0.7.9-0.815.1mdv2009.0
+ Revision: 206955
- br gnome-doc-utils
- re-enable libburn plugins (work with current libburnia now)
- new snapshot 815

* Wed Apr 23 2008 Adam Williamson <awilliamson@mandriva.org> 0.7.9-0.761.1mdv2009.0
+ Revision: 196792
- add desktop.patch to fix an error in the .desktop file
- disable libburnia temporarily as libisofs 0.6 is not yet supported
- switch to SVN trunk

* Wed Mar 26 2008 Adam Williamson <awilliamson@mandriva.org> 0.7.2-0.693.1mdv2008.1
+ Revision: 190209
- buildrequires libusb-devel
- add Dutch translation by Fred Himpe from SVN head (#39392)
- bump to rev 693 (updates for many translations, adds Greek translation)

* Thu Feb 28 2008 Adam Williamson <awilliamson@mandriva.org> 0.7.2-0.643.2mdv2008.1
+ Revision: 176491
- drop workarounds for some issues that have now been fixed upstream
- update to current snapshot of stable branch (upstream blesses it as stable, contains important fixes for 0.7.1)

  + Thierry Vignaud <tv@mandriva.org>
    - fix gstreamer0.10-devel BR for x86_64

* Sat Feb 09 2008 Emmanuel Andry <eandry@mandriva.org> 0.7.1-2mdv2008.1
+ Revision: 164495
- rebuild for new libcamel

* Mon Jan 28 2008 Adam Williamson <awilliamson@mandriva.org> 0.7.1-1mdv2008.1
+ Revision: 158932
- fix bogus : separator in .desktop file
- disable the glibc workaround, doesn't seem to be right any more
- new release 0.7.1

* Thu Dec 27 2007 Jérôme Soyer <saispo@mandriva.org> 0.7.0-1mdv2008.1
+ Revision: 138353
- New release 0.7.0

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request
    - do not package big ChangeLog

* Fri Dec 07 2007 Funda Wang <fwang@mandriva.org> 0.6.90-2mdv2008.1
+ Revision: 116123
- rebuild for new beagle

* Tue Nov 27 2007 Adam Williamson <awilliamson@mandriva.org> 0.6.90-1mdv2008.1
+ Revision: 113509
- fix file list again
- fix file list
- drop both patches, merged upstream
- new release 0.6.90

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - fix buildrequires
    - fix desktop entry

* Sat Nov 17 2007 Funda Wang <fwang@mandriva.org> 0.6.1-7mdv2008.1
+ Revision: 109293
- rebuild for new lzma

* Mon Nov 05 2007 Funda Wang <fwang@mandriva.org> 0.6.1-6mdv2008.1
+ Revision: 105956
- rebuild for new totem

* Fri Sep 28 2007 Adam Williamson <awilliamson@mandriva.org> 0.6.1-5mdv2008.0
+ Revision: 93487
- add brasero-0.6.1-sectorsize.patch from upstream SVN to fix size calculation for audio and VCDs (so long audio and VCDs do not fail due to being 'too big')

* Thu Sep 20 2007 Adam Williamson <awilliamson@mandriva.org> 0.6.1-4mdv2008.0
+ Revision: 91672
- adjust XDG categories (fix #33828)

* Wed Sep 19 2007 Pascal Terjan <pterjan@mandriva.org> 0.6.1-3mdv2008.0
+ Revision: 90806
- Bump release to re-upload lost package

* Sun Sep 09 2007 Pascal Terjan <pterjan@mandriva.org> 0.6.1-2mdv2008.0
+ Revision: 83451
- Fix release
- rebuild

* Sat Aug 25 2007 Funda Wang <fwang@mandriva.org> 0.6.1-1mdv2008.0
+ Revision: 71294
- 0.6.1 stable

* Tue Aug 14 2007 Adam Williamson <awilliamson@mandriva.org> 0.6.1-0.283.1mdv2008.0
+ Revision: 63486
- update to SVN rev 283 to fix an upstream booboo that was breaking compile
- correct category addition (no semi-colon when using desktop-file-install)
- correct license to GPLv2+
- update to latest 0.6 branch SVN: fixes for some important bugs

* Tue Jul 31 2007 Adam Williamson <awilliamson@mandriva.org> 0.6.0-2mdv2008.0
+ Revision: 57171
- fix and improve description

* Tue Jul 31 2007 Adam Williamson <awilliamson@mandriva.org> 0.6.0-1mdv2008.0
+ Revision: 57160
- buildrequires libgcrypt-devel
- fix for glibc 2.6 change to sg
- add patch0 to enable deprecated APIs (needed to build against GTK+ 2.11.6)
- update URL
- 0.6.0 final

* Tue Jul 03 2007 Adam Williamson <awilliamson@mandriva.org> 0.6.0-0.245.1mdv2008.0
+ Revision: 47614
- update to current SVN; build against libburn and libisofs

  + Götz Waschk <waschk@mandriva.org>
    - fix script syntax

* Tue Apr 17 2007 Jérôme Soyer <saispo@mandriva.org> 0.5.90-1mdv2008.0
+ Revision: 13611
- New release 0.5.90

