Summary:	Authoring and playing system for educational activities
Name:		jclic
Group:		Education
Version:	0.2.1.0
Release:	%mkrel 1
License:	GPL
Url:		http://projectes.lafarga.cat/projects/jclic
Source0:	http://projectes.lafarga.cat/projects/jclic/downloads/files/4342/jclic-0.2.1.0-src.zip
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

#-------------------------------------------------------------------------------
BuildRequires:	ant
BuildRequires:	ant-nodeps
BuildRequires:	imagemagick
BuildRequires:	java-rpmbuild
BuildRequires:	jpackage-utils

#-------------------------------------------------------------------------------
%description
JClic is a set of cross-platform Java applications useful for creating
and carrying out different types of educational activities like puzzles,
associations, text exercises or crosswords.

#-----------------------------------------------------------------------
%prep
%setup -q -n %{name}-%{version}-src

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
java -jar %{_datadir}/%{name}/%{name}/jclic.jar
EOF
cat > %{buildroot}%{_bindir}/jclicauthor << EOF
#!/bin/sh
java -Xmx256m -jar %{_datadir}/%{name}/%{name}/jclicauthor.jar
EOF
cat > %{buildroot}%{_bindir}/jclicreports << EOF
#!/bin/sh
java -jar %{_datadir}/%{name}/%{name}/jclicreports.jar
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
cat > %{buildroot}%{_datadir}/applications/mandriva-$name.desktop << EOF
[Desktop Entry]
Name=$name
Comment=Authoring and playing system for educational activities
Exec=$name
Icon=%{name}
Terminal=false
Type=Application
Categories=Education
EOF
    done
popd

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
