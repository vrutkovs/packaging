%global required_pulp_version 2.13

Name: pulp-docker
Version: 2.4.0
Release: 5.manifestlists%{?dist}
BuildArch: noarch

License:   GPLv2+
Summary:   Support for Docker content in the Pulp platform
URL:       https://github.com/pulp/pulp_docker
Source0:   https://github.com/pulp/pulp_docker/archive/%{name}-%{version}-1.tar.gz
Patch0:    pulp-docker-manifest-lists-support.patch

BuildRequires: python2-devel
BuildRequires: python-setuptools
BuildRequires: python-sphinx


%description
Provides a collection of Pulp server plugins and admin client extensions to
support Docker content.


%prep
%autosetup -n pulp_docker-%{name}-%{version}-1 -p1
%patch0 -p1

%build
for directory in $(find . -type f -name "setup.py" | xargs dirname)
do
    pushd $directory
    %py2_build
    popd
done

pushd docs
make %{?_smp_mflags} html
# We don't want to install the objects.inv, because it is a build-time database
rm _build/html/objects.inv
popd


%install
for directory in $(find . -type f -name "setup.py" | xargs dirname)
do
    pushd $directory
    %py2_install
    popd
done

install -d %{buildroot}/%{_sysconfdir}/httpd/conf.d/
install -d %{buildroot}/%{_sysconfdir}/pulp/server/plugins.conf.d/
install -d %{buildroot}/%{_var}/lib/pulp/published/docker/

install -pm644 plugins/etc/httpd/conf.d/* %{buildroot}/%{_sysconfdir}/httpd/conf.d/
install -pm644 plugins/etc/pulp/server/plugins.conf.d/* \
    %{buildroot}/%{_sysconfdir}/pulp/server/plugins.conf.d/


# ---- Admin Extensions --------------------------------------------------------
%package admin-extensions
Summary: The Pulp Docker admin client extensions
Requires: pulp-admin-client >= %{required_pulp_version}
Requires: python2-pulp-docker-common = %{version}


%description admin-extensions
pulp-admin extensions for Docker support


%files admin-extensions
%license LICENSE
%doc AUTHORS COPYRIGHT
%{python_sitelib}/pulp_docker/extensions/admin/
%{python_sitelib}/pulp_docker_extensions_admin*.egg-info


# ---- Docker Documentation-----------------------------------------------------
%package doc
Summary: Pulp Docker documentation


%description doc
Documentation for the Pulp Docker plugins.


%files doc
%license LICENSE
%doc AUTHORS COPYRIGHT
%doc docs/_build/html/*


# ---- Plugins -----------------------------------------------------------------
%package plugins
Summary: Pulp Docker plugins
Requires: pulp-server >= %{required_pulp_version}
Requires: python-nectar >= 1.3.0
Requires: python2-pulp-docker-common = %{version}
Requires: rsync


%description plugins
Provides a collection of platform plugins that extend the Pulp platform
to provide Docker specific support


%files plugins
%license LICENSE
%doc AUTHORS COPYRIGHT
%config(noreplace) %{_sysconfdir}/httpd/conf.d/pulp_docker.conf
%config(noreplace) %{_sysconfdir}/pulp/server/plugins.conf.d/docker_distributor_export.json
%config(noreplace) %{_sysconfdir}/pulp/server/plugins.conf.d/docker_distributor.json
%{python_sitelib}/pulp_docker/plugins/
%{python_sitelib}/pulp_docker_plugins*.egg-info
%attr(-, apache, apache) %dir %{_var}/lib/pulp/published/docker


# ---- Docker Common -----------------------------------------------------------
%package -n python2-pulp-docker-common
Summary: Pulp Docker support common library
Requires: python2-pulp-common >= %{required_pulp_version}
%{?python_provide:%python_provide python2-pulp-docker-common}


%description -n python2-pulp-docker-common
Common libraries for python2-pulp-docker


%files -n python2-pulp-docker-common
%license LICENSE
%doc AUTHORS COPYRIGHT
%dir %{python_sitelib}/pulp_docker
%{python_sitelib}/pulp_docker/__init__.py*
%{python_sitelib}/pulp_docker/common/
%dir %{python_sitelib}/pulp_docker/extensions
%{python_sitelib}/pulp_docker/extensions/__init__.py*
%{python_sitelib}/pulp_docker_common*.egg-info


%changelog
* Thu Jul 13 2017 Vadim Rutkovsky <vrutkovs@redhat.com> - 2.4.0-4.manifestlists
- Add manifest list support patch

* Wed Jun 21 2017 Patrick Creech <pcreech@redhat.com> - 2.4.0-1
- Update to 2.4.0

* Mon Feb 27 2017 Bihan Zhang <bizhang@redhat.com> - 2.3.0-1
- Update to 2.3.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Wed Sep 21 2016 Patrick Creech <pcreech@redhat.com> - 2.1.0-2
- Remove trailing .0 on pulp_version

* Wed Sep 21 2016 Patrick Creech <pcreech@redhat.com> - 2.1.0-1
- Update to 2.1.0
- Adding rsync dependency

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.2-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jul 14 2016 Jeremy Cline <jcline@redhat.com> - 2.0.2-1
- Update to 2.0.2

* Mon May 16 2016 Randy Barlow <rbarlow@redhat.com> - 2.0.1-1
- Update to 2.0.1 (#1337316).
- Change the license to GPLv2+ as per the upstream COPYRIGHT file.
- Remove unneeded python2-setuptools dependency.

* Thu Mar 17 2016 Randy Barlow <rbarlow@redhat.com> - 2.0.0-1
- Update to the 2.0.0 release.

* Wed Mar 09 2016 Randy Barlow <rbarlow@redhat.com> - 2.0.0-0.9.rc.1
- Update to the 2.0.0 release candidate.

* Fri Mar 04 2016 Randy Barlow <rbarlow@redhat.com> - 2.0.0-0.7.beta.1
- Update to the seventh beta.
- Corrected the summary and description on the documentation subpackage.
- Depend on python2-rpm-macros instead of rpm-python.
- No longer need to rm the tests since that was fixed upstream.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-0.4.beta.1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 29 2016 Jeremy Cline <jeremy@jcline.org> - 2.0.0-0.4.beta.1
- Raise to the fourth beta.

* Thu Jan 21 2016 Randy Barlow <rbarlow@redhat.com> - 2.0.0-0.3.beta.1
- Raise to the third beta.
- Remove usage of defattr, using install to set ownership instead.

* Mon Jan 11 2016 Randy Barlow <rbarlow@redhat.com> 2.0.0-0.1.beta.1
- Initial release.
