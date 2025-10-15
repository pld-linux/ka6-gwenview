#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.08.2
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		gwenview
Summary:	Simple image viewer
Summary(pl.UTF-8):	Prosta przeglądarka obrazów
Name:		ka6-%{kaname}
Version:	25.08.2
Release:	3
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	fa0d649825476b965ad56bc49a452ef5
URL:		https://kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6MultimediaWidgets-devel >= %{qtver}
BuildRequires:	cfitsio-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	exiv2-devel
BuildRequires:	gettext-tools
BuildRequires:	kColorPicker-qt6-devel
BuildRequires:	kImageAnnotator-qt6-devel
BuildRequires:	ka6-libkdcraw-devel >= %{kdeappsver}
BuildRequires:	kf6-baloo-devel >= %{kframever}
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kiconthemes-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-kparts-devel >= %{kframever}
BuildRequires:	kf6-purpose-devel >= %{kframever}
BuildRequires:	lcms2-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	python
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRequires:	zlib-devel
Requires:	%{name}-data = %{version}-%{release}
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-%{kaname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Gwenview is an image viewer for KDE.

It features a folder tree window and a file list window to provide
easy navigation in your file hierarchy. Image loading is done by the
Qt library, so it supports all image formats your Qt installation
supports.

%description -l pl.UTF-8
Gwenview to przeglądarka obrazków dla KDE.

Wyświetla ona drzewiastą strukturę folderów i okno z listą plików do
łatwego nawigowania po hieracrchi plików. Ładowanie obrazków jest
wykonywane przez bibliotę Qt, więc obsługiwane są wszystkie formaty
obrazów, które wspiera Qt.

%package data
Summary:	Data files for %{kaname}
Summary(pl.UTF-8):	Dane dla %{kaname}
Group:		X11/Applications
Requires(post,postun):	desktop-file-utils
Obsoletes:	ka5-%{kaname}-data < %{version}
BuildArch:	noarch

%description data
Data files for %{kaname}.

%description data -l pl.UTF-8
Dane dla %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

rm -rf $RPM_BUILD_ROOT%{_kdedocdir}/sr
# not supported by glibc yet
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post data
%update_desktop_database_post

%postun data
%update_desktop_database_postun


%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/gwenview
%attr(755,root,root) %{_bindir}/gwenview_importer
%{_libdir}/libgwenviewlib.so.*.*
%ghost %{_libdir}/libgwenviewlib.so.5
%{_libdir}/qt6/plugins/kf6/kfileitemaction/slideshowfileitemaction.so
%{_libdir}/qt6/plugins/kf6/parts/gvpart.so

%files data -f %{kaname}.lang
%defattr(644,root,root,755)
%{_desktopdir}/org.kde.gwenview.desktop
%{_desktopdir}/org.kde.gwenview_importer.desktop
%{_datadir}/gwenview
%{_iconsdir}/hicolor/*x*/*/*.png
%{_datadir}/metainfo/org.kde.gwenview.appdata.xml
%{_datadir}/qlogging-categories6/gwenview.categories
%{_datadir}/solid/actions/gwenview_importer.desktop
%{_datadir}/solid/actions/gwenview_importer_camera.desktop
