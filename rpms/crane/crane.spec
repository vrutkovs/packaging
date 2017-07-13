%global sum A WSGI app providing a docker-registry-like API with redirection
%global desc This WSGI application exposes a read-only API similar to \
docker-registry, which docker can use for "docker pull" operations. \
Requests for actual image files are responded to with 302 redirects to \
a URL formed with per-repository settings.


Name: python-crane
Version: 2.1.0
Release: 1.manifestlists%{?dist}

License:   GPLv2+
Summary:   %{sum}
URL:       https://github.com/pulp/crane
Source0:   https://github.com/pulp/crane/archive/python-crane-%{version}-1.tar.gz
Patch1:    0001-Update-to-latest-master.patch
Patch2:    0002-manifest-lists-support.patch
BuildArch: noarch

BuildRequires: python2-devel
BuildRequires: python-setuptools


%description
%desc


%package -n python2-crane
Summary: %{sum}
Requires: python-flask >= 0.9
Requires: python-rhsm
Requires: python2-setuptools
Requires(post): policycoreutils-python
Requires(postun): policycoreutils-python

# This upstream issue tracks the bundling of fonts: https://pulp.plan.io/issues/1516
# Until that is resolved, we will mark the fonts as bundled.
Provides: bundled(fontawesome-fonts-web)
Provides: bundled(open-sans-fonts)
# This font does not seem to be in Fedora, so I'm guessing at its name. Accoding to
# https://www.patternfly.org/styles/typography/ it is licensed Creative Commons Attribution 4.0
# International license.
Provides: bundled(patternflyicons-fonts-web)
%{?python_provide:%python_provide python2-crane}


%description -n python2-crane
%desc


%prep
%autosetup -n crane-python-crane-%{version}-1 -p1


%build
%py2_build


%install
%py2_install

install -d %{buildroot}/%{_datadir}/crane/
install -d %{buildroot}/%{_var}/lib/crane/metadata/

install -pm644 deployment/crane.wsgi %{buildroot}/%{_datadir}/crane/

install -pm644 deployment/apache24.conf %{buildroot}/%{_datadir}/crane/apache.conf
install -pm644 deployment/crane.wsgi %{buildroot}/%{_datadir}/crane/


%files -n python2-crane
%license COPYRIGHT LICENSE
%doc AUTHORS README.rst
%{python2_sitelib}/crane
%{python2_sitelib}/crane*.egg-info
%{_datadir}/crane/
%dir %{_var}/lib/crane/


%post
if /usr/sbin/selinuxenabled; then
    semanage fcontext -a -t httpd_sys_content_t '%{_var}/lib/crane(/.*)?'
    restorecon -R -v %{_var}/lib/crane
fi


%postun
if [ $1 -eq 0 ] ; then  # final removal
    if /usr/sbin/selinuxenabled; then
        semanage fcontext -d -t httpd_sys_content_t '%{_var}/lib/crane(/.*)?'
        restorecon -R -v %{_var}/lib/crane
    fi
fi


%changelog
* Thu Jul 13 2017 Vadim Rutkovsky <vrutkovs@redhat.com> - 2.1.0-1.manifestlists
- Add manifest list support patch

* Wed Jun 21 2017 Patrick Creech <pcreech@redhat.com> - 2.1.0-1
- new version

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Fri Aug 19 2016 Jeremy Cline <jcline@redhat.com> - 2.0.2-1
- Update to 2.0.2

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.0-3
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Tue May 17 2016 Randy Barlow <rbarlow@redhat.com> - 2.0.0-2
- Change the license to GPLv2+ as per the COPYRIGHT file.

* Fri Mar 18 2016 Randy Barlow <rbarlow@redhat.com> - 2.0.0-1
- Update to 2.0.0.

* Wed Mar 09 2016 Randy Barlow <rbarlow@redhat.com> - 2.0.0-0.9.rc.1
- Update to the 2.0.0 release candidate.

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.0.0-0.4.beta.1.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Fri Jan 29 2016 Jeremy Cline <jeremy@jcline.com> 2.0.0-0.4.beta.1
- Bump to the fourth beta release of 2.0.0.

* Mon Jan 11 2016 Randy Barlow <rbarlow@redhat.com> 2.0.0-0.1.beta.1
- Initial release.
