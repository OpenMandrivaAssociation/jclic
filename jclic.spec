Summary:	Authoring and playing system for educational activities
Name:		jclic
Group:		Education
Version:	0.2.1.0
Release:	%mkrel 4
License:	GPL
Url:		https://projectes.lafarga.cat/projects/jclic
Source0:	http://projectes.lafarga.cat/projects/jclic/downloads/files/4342/jclic-0.2.1.0-src.zip
Source1:	jclic.1
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

#-------------------------------------------------------------------------------
BuildRequires:	ant
BuildRequires:	ant-jmf
BuildRequires:	ant-nodeps
BuildRequires:	imagemagick
BuildRequires:	java-rpmbuild
BuildRequires:	jpackage-utils
Requires:	fmj
Requires:	tritonus

#-------------------------------------------------------------------------------
# Auto detect/use pt_BR instead of pt_PT; should work on other locale variants
Patch0:		jclic-0.2.1.0-locale.patch

# Default to xgd-open instead of mozilla
Patch1:		jclic-0.2.1.0-browser.patch

#-------------------------------------------------------------------------------
%description
JClic is a set of cross-platform Java applications useful for creating
and carrying out different types of educational activities like puzzles,
associations, text exercises or crosswords.

#-----------------------------------------------------------------------
%prep
%setup -q -n %{name}-%{version}-src

%patch0 -p1
%patch1 -p1

#-----------------------------------------------------------------------
%build
JAVA_HOME=%{java_home} ant

#-----------------------------------------------------------------------
%install
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -far dist/* %{buildroot}%{_datadir}/%{name}
pushd %{buildroot}%{_datadir}/%{name}/%{name}
    rm -fr %{buildroot}%{_datadir}/%{name}/icons
    rm -f %{buildroot}%{_datadir}/%{name}/jclic-icons.zip
    rm -f %{buildroot}%{_datadir}/%{name}/jclic-aqua-icons.sit
popd

mkdir -p %{buildroot}%{_bindir}
cat > %{buildroot}%{_bindir}/jclic << EOF
#!/bin/sh
LD_LIBRARY_PATH=%{_libdir}/fmj java -classpath %{_datadir}/%{name}/%{name}/jclic.jar:\`%{_bindir}/build-classpath fmj\` JClicPlayer "\$@"
EOF
cat > %{buildroot}%{_bindir}/jclicauthor << EOF
#!/bin/sh
java -Xmx256m -jar %{_datadir}/%{name}/%{name}/jclicauthor.jar "\$@"
EOF
cat > %{buildroot}%{_bindir}/jclicreports << EOF
#!/bin/sh
java -jar %{_datadir}/%{name}/%{name}/jclicreports.jar "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/*

mkdir -p %{buildroot}{%{_miconsdir},%{_iconsdir},%{_datadir}/pixmaps}
mkdir -p %{buildroot}%{_datadir}/applications
pushd dist/jclic/icons
    for app in "" author reports; do
    name=%{name}$app
    if [ -z "$app" ]; then
	file=$name.png
    else
	file=$app.png
    fi
    icon=$name.png
    convert -resize 16x16 $file %{buildroot}%{_miconsdir}/$icon
    convert -resize 32x32 $file %{buildroot}%{_iconsdir}/$icon
    install -m644 -D $file %{buildroot}%{_liconsdir}/$icon
    case $app in
	author)		desk="JClic Author"		;;
	reports)	desk="JClic Report Server"	;;
	*)		desk="JClic"			;;
    esac
cat > %{buildroot}%{_datadir}/applications/mandriva-$name.desktop << EOF
[Desktop Entry]
Name=$desk
Comment=Authoring and playing system for educational activities
Exec=$name
Icon=$icon
Terminal=false
Type=Application
Categories=Education;
EOF
    done
popd

mkdir -p %{buildroot}%{_mandir}/man1
cp %{SOURCE1} %{buildroot}%{_mandir}/man1
xz -z %{buildroot}%{_mandir}/man1/jclic.1

#-----------------------------------------------------------------------
%clean
rm -rf %{buildroot}

#-----------------------------------------------------------------------
%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/%{name}
%{_miconsdir}/*.png
%{_iconsdir}/*.png
%{_liconsdir}/*.png
%{_datadir}/applications/*.desktop
%{_mandir}/man1/jclic.1*


%changelog
* Sat Jan 08 2011 Paulo Andrade <pcpa@mandriva.com.br> 0.2.1.0-4mdv2011.0
+ Revision: 630388
- Add requires of tritonus meta-package to install all media handlers
- Correct generation of the jclic script by escaping backquote in spec

* Fri Jan 07 2011 Paulo Andrade <pcpa@mandriva.com.br> 0.2.1.0-3mdv2011.0
+ Revision: 629682
- Use fmj instead of missing requirement of jfm

* Thu Jan 06 2011 Paulo Andrade <pcpa@mandriva.com.br> 0.2.1.0-2mdv2011.0
+ Revision: 629180
- Automatically detect locale country
- Use xdg-open as default browser
- Add debian jclic manpage

* Wed Jan 05 2011 Paulo Andrade <pcpa@mandriva.com.br> 0.2.1.0-1mdv2011.0
+ Revision: 628855
- Import jclic 0.2.1.0
- jclic

