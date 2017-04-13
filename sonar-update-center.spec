%{?_javapackages_macros:%_javapackages_macros}

Name:           sonar-update-center
Version:        1.12.1
Release:        8%{?dist}
Summary:        Sonar Update Center
Group:          Development/Java
License:        LGPLv3+
URL:            http://www.sonarqube.org
Source0:        https://github.com/SonarSource/%{name}/archive/%{version}.tar.gz

Patch0:         0001-Port-to-current-maven-dependency-tree.patch

BuildArch:      noarch

BuildRequires:  maven-local
BuildRequires:  mvn(com.google.code.findbugs:jsr305)
BuildRequires:  mvn(com.google.guava:guava)
BuildRequires:  mvn(commons-io:commons-io)
BuildRequires:  mvn(commons-lang:commons-lang)
BuildRequires:  mvn(org.apache.maven:maven-archiver)
BuildRequires:  mvn(org.apache.maven:maven-core)
BuildRequires:  mvn(org.apache.maven:maven-plugin-api)
BuildRequires:  mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:  mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:  mvn(org.apache.maven.shared:maven-dependency-tree)
BuildRequires:  mvn(org.slf4j:slf4j-api)

%description
Update center for Sonar - platform for continuous inspection of code quality.

%package -n sonar-packaging-maven-plugin
Summary:        Maven plugin for building Sonar plugins

%description -n sonar-packaging-maven-plugin
Maven plugin for building Sonar plugins.

%package javadoc
Summary:        Javadoc for %{name}

%description javadoc
This package contains javadoc for %{name}.

%prep
%setup -q

#patch0 -p1

find -name '*.jar' -delete

# circular dependency - parent is part of sonar-plugins which needs
# sonar-packaging-maven-plugin to build
%pom_remove_parent

# missing org.freemarker:freemaker and com.github.kevinsawicki:http-request
%pom_disable_module sonar-update-center-mojo

# guava stopped reexporting @Nullable
%pom_add_dep com.google.code.findbugs:jsr305

%mvn_package :sonar-packaging-maven-plugin sonar-packaging-maven-plugin

%build
# missing fest-assert
%mvn_build -f

%install
%mvn_install

%files -f .mfiles
%dir %{_javadir}/%{name}

%files -n sonar-packaging-maven-plugin -f .mfiles-sonar-packaging-maven-plugin

%files javadoc -f .mfiles-javadoc

%changelog
* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Michael Simacek <msimacek@redhat.com> - 1.12.1-7
- Regenerate buildrequires

* Fri Feb 05 2016 Fedora Release Engineering <releng@fedoraproject.org> - 1.12.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Nov 23 2015 Michael Simacek <msimacek@redhat.com> - 1.12.1-5
- Port to current maven-dependency-tree

* Fri Jun 19 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.12.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue May 19 2015 Michael Simacek <msimacek@redhat.com> - 1.12.1-3
- Fix FTBFS

* Fri Oct 24 2014 Michael Simacek <msimacek@redhat.com> - 1.12.1-2
- Removed separate license text (not needed for LGPL)

* Thu Oct 23 2014 Michael Simacek <msimacek@redhat.com> - 1.12.1-1
- Initial version
