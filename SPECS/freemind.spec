Name:		freemind
Version:	1.0.1
Release:	1%{?dist}
Summary:	Mind-mapping software

Group:          Applications/Productivity
License:        GPLv2	
URL:		http://freemind.sourceforge.net
Source0:	http://freefr.dl.sourceforge.net/project/freemind/freemind/1.0.1/freemind-bin-1.0.1.zip
Source1:        freemind.desktop
Source2:        freemind.xml
#Source3:        FreeMindWindowIcon.png

BuildArch:      noarch
BuildRequires:  desktop-file-utils
BuildRequires:  ImageMagick
Requires:       hicolor-icon-theme
Requires:       java >= 1:1.6.0
Requires:       unzip

%description
Freemind is a mind-mapping sofware written in Java.

%prep
%setup -q -c

%install
install -d $RPM_BUILD_ROOT%{_bindir} \
           $RPM_BUILD_ROOT%{_datadir}/%{name} \
           $RPM_BUILD_ROOT%{_datadir}/%{name}/accesories \
           $RPM_BUILD_ROOT%{_datadir}/%{name}/doc \
           $RPM_BUILD_ROOT%{_datadir}/%{name}/lib

install -m 755 freemind.sh $RPM_BUILD_ROOT%{_bindir}/%{name}

cp license $RPM_BUILD_ROOT%{_datadir}/%{name}/
cp *.ortho dictionaries.properties $RPM_BUILD_ROOT%{_datadir}/%{name}/
cp patterns.xml $RPM_BUILD_ROOT%{_datadir}/%{name}/
cp -pr lib/* $RPM_BUILD_ROOT%{_datadir}/%{name}/lib/
cp -pr doc/* $RPM_BUILD_ROOT%{_datadir}/%{name}/doc/

desktop-file-install --dir %{buildroot}%{_datadir}/applications %{SOURCE1}

unzip lib/freemind.jar \*/FreeMindWindowIcon.png

mkdir -p %{buildroot}%{_datadir}/pixmaps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/16x16/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/32x32/apps
mkdir -p %{buildroot}%{_datadir}/icons/hicolor/48x48/apps

convert -scale 32 images/FreeMindWindowIcon.png %{buildroot}%{_datadir}/pixmaps/%{name}.png

for i in 16 32 48
do
   convert -scale $i images/FreeMindWindowIcon.png %{buildroot}%{_datadir}/icons/hicolor/${i}x${i}/apps/%{name}.png
done

mkdir -p %{buildroot}%{_datadir}/mime/packages
cp -a %{SOURCE2} %{buildroot}%{_datadir}/mime/packages/

%post
update-desktop-database /usr/share/applications &> /dev/null || :

touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :
touch --no-create %{_datadir}/mime/packages &>/dev/null || :

%postun
update-desktop-database /usr/share/applications &> /dev/null || :

if [ $1 -eq 0 ] ; then
    touch --no-create %{_datadir}/icons/hicolor &>/dev/null
    gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
    update-mime-database %{_datadir}/mime &> /dev/null || :
fi

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
update-mime-database %{?fedora:-n} %{_datadir}/mime &> /dev/null || :

%files
%{_datadir}/applications/*%{name}.desktop
%{_datadir}/mime/packages/%{name}.xml
%{_datadir}/pixmaps/%{name}.png
%{_datadir}/icons/hicolor/16x16/apps/%{name}.png
%{_datadir}/icons/hicolor/32x32/apps/%{name}.png
%{_datadir}/icons/hicolor/48x48/apps/%{name}.png
%{_bindir}/%{name}
%{_datadir}/%{name}
%doc license

%changelog
* Thu May 26 2016 Ricardo Arguello <rarguello@deskosproject.org>
- Initial package for DeskOS
