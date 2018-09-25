# Macros for py2/py3 compatibility
%if 0%{?fedora} || 0%{?rhel} > 7
%global pyver %{python3_pkgversion}
%else
%global pyver 2
%endif
%global pyver_bin python%{pyver}
%global pyver_sitelib %python%{pyver}_sitelib
%global pyver_install %py%{pyver}_install
%global pyver_build %py%{pyver}_build
# End of macros for py2/py3 compatibility
%global pypi_name tacker
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
OpenStack Tacker Service is an NFV Orchestrator for OpenStack

# FIXME(ykarel) Disable doc build until sphinxcontrib-apidoc package is available
# https://review.rdoproject.org/r/#/c/13280/
%global with_doc 0

Name:           openstack-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack Tacker Service

License:        ASL 2.0
URL:            https://launchpad.net/%{pypi_name}
Source0:        http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source1:        openstack-tacker-server.service
Source2:        tacker.logrotate
Source3:        openstack-tacker-conductor.service

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  systemd
BuildRequires:  python%{pyver}-castellan
BuildRequires:  python%{pyver}-devel
BuildRequires:  python%{pyver}-setuptools
BuildRequires:  python%{pyver}-eventlet
BuildRequires:  python%{pyver}-heatclient
BuildRequires:  python%{pyver}-heat-translator
BuildRequires:  python%{pyver}-mistralclient
BuildRequires:  python%{pyver}-neutronclient
BuildRequires:  python%{pyver}-oslo-config
BuildRequires:  python%{pyver}-oslo-log
BuildRequires:  python%{pyver}-oslo-db
BuildRequires:  python%{pyver}-oslo-policy
BuildRequires:  python%{pyver}-oslo-service
BuildRequires:  python%{pyver}-oslo-messaging
BuildRequires:  python%{pyver}-paramiko
BuildRequires:  python%{pyver}-routes
BuildRequires:  python%{pyver}-tosca-parser
BuildRequires:  python%{pyver}-webob
BuildRequires:  python%{pyver}-barbicanclient
BuildRequires:  openstack-macros
BuildRequires:  python%{pyver}-kubernetes
BuildRequires:  PyYAML
# Test dependencies
BuildRequires:  python%{pyver}-cliff
BuildRequires:  python%{pyver}-fixtures
BuildRequires:  python%{pyver}-hacking
BuildRequires:  python%{pyver}-mock
BuildRequires:  python%{pyver}-oslotest
# For Fedora, the ostestr binary is provided by the python3 subpackage
BuildRequires:  /usr/bin/ostestr
BuildRequires:  python%{pyver}-subunit
BuildRequires:  python%{pyver}-tackerclient
BuildRequires:  python%{pyver}-tempest
BuildRequires:  python%{pyver}-testrepository
BuildRequires:  python%{pyver}-testtools

# Handle python2 exception
%if %{pyver} == 2
BuildRequires:  python-webtest
%else
BuildRequires:  python%{pyver}-webtest
%endif

Requires: openstack-%{pypi_name}-common = %{version}-%{release}

Requires(pre): shadow-utils
%{?systemd_requires}

%description
%{common_desc}

%package -n     python%{pyver}-%{pypi_name}
Summary:        OpenStack Tacker Service
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}}

Requires: python%{pyver}-routes
Requires: python%{pyver}-babel
Requires: python%{pyver}-castellan
Requires: python%{pyver}-eventlet
Requires: python%{pyver}-requests
Requires: python%{pyver}-keystonemiddleware >= 4.17.0
Requires: python%{pyver}-kombu
Requires: python%{pyver}-netaddr
Requires: python%{pyver}-sqlalchemy
Requires: python%{pyver}-webob
Requires: python%{pyver}-heatclient >= 1.10.0
Requires: python%{pyver}-keystoneclient >= 1:3.8.0
Requires: python%{pyver}-alembic
Requires: python%{pyver}-six
Requires: python%{pyver}-stevedore
Requires: python%{pyver}-oslo-concurrency >= 3.26.0
Requires: python%{pyver}-oslo-config >= 2:5.2.0
Requires: python%{pyver}-oslo-context >= 2.19.2
Requires: python%{pyver}-oslo-db >= 4.27.0
Requires: python%{pyver}-oslo-log >= 3.36.0
Requires: python%{pyver}-oslo-messaging >= 5.29.0
Requires: python%{pyver}-oslo-middleware >= 3.31.0
Requires: python%{pyver}-oslo-policy >= 1.30.0
Requires: python%{pyver}-oslo-reports >= 1.18.0
Requires: python%{pyver}-oslo-rootwrap >= 5.8.0
Requires: python%{pyver}-oslo-serialization >= 2.18.0
Requires: python%{pyver}-oslo-service >= 1.24.0
Requires: python%{pyver}-oslo-utils >= 3.33.0
Requires: python%{pyver}-mistralclient >= 3.1.0
Requires: python%{pyver}-neutronclient >= 6.7.0
Requires: python%{pyver}-novaclient >= 9.1.0
Requires: python%{pyver}-tosca-parser >= 0.8.1
Requires: python%{pyver}-heat-translator >= 1.1.0
Requires: python%{pyver}-cryptography
Requires: python%{pyver}-paramiko
Requires: python%{pyver}-pyroute2
Requires: python%{pyver}-barbicanclient >= 4.5.2
Requires: python%{pyver}-pbr
Requires: python%{pyver}-kubernetes

# Handle python2 exception
%if %{pyver} == 2
Requires: python-paste
Requires: python-paste-deploy
Requires: python-anyjson
Requires: PyYAML
%else
Requires: python%{pyver}-paste
Requires: python%{pyver}-paste-deploy
Requires: python%{pyver}-anyjson
Requires: python%{pyver}-PyYAML
%endif

%description -n python%{pyver}-%{pypi_name}
%{common_desc}

This package contains the Tacker python library.

%package common
Summary:  %{pypi_name} common files
Requires: python%{pyver}-%{pypi_name} = %{version}-%{release}

%description common
%{common_desc}

This package contains the Tacker common files.

%package -n python%{pyver}-%{pypi_name}-tests
Summary:    Tacker unit and functional tests
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}-tests}
Requires:   python%{pyver}-%{pypi_name} = %{version}-%{release}

Requires:  python%{pyver}-cliff
Requires:  python%{pyver}-fixtures
Requires:  python%{pyver}-mock
Requires:  python%{pyver}-oslotest
Requires:  python%{pyver}-os-testr
Requires:  python%{pyver}-subunit
Requires:  python%{pyver}-tackerclient
Requires:  python%{pyver}-tempest
Requires:  python%{pyver}-testrepository
Requires:  python%{pyver}-testtools

# Handle python2 exception
%if %{pyver} == 2
Requires:  python-webtest
%else
Requires:  python%{pyver}-webtest
%endif

%description -n python%{pyver}-%{pypi_name}-tests
%{common_desc}

This package contains the Tacker unit and functional test files.

%if 0%{?with_doc}
%package -n python%{pyver}-%{pypi_name}-doc
Summary:    Documentation for OpenStack Tacker service
%{?python_provide:%python_provide python%{pyver}-%{pypi_name}-doc}

BuildRequires:  python%{pyver}-sphinx
BuildRequires:  python%{pyver}-openstackdocstheme
BuildRequires:  python%{pyver}-oslo-reports
BuildRequires:  python%{pyver}-mistral

%description -n python%{pyver}-%{pypi_name}-doc
Documentation for OpenStack Tacker service
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{pyver_build}

# Generate sample config and add the current directory to PYTHONPATH so
# oslo-config-generator-%{pyver} doesn't skip tacker entry points.
PYTHONPATH=. oslo-config-generator-%{pyver} --config-file=./etc/config-generator.conf --output-file=./etc/%{pypi_name}.conf

%if 0%{?with_doc}
# generate html docs
# (TODO) Remove -W option (warning-is-error) until https://review.openstack.org/#/c/557728 is
# merged.
sphinx-build-%{pyver} -b html doc/source doc/build/html
# remove the sphinx-build-%{pyver} leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}
%endif

%install
%{pyver_install}

# Setup directories
install -d -m 755 %{buildroot}%{_datadir}/%{pypi_name}
install -d -m 755 %{buildroot}%{_sharedstatedir}/%{pypi_name}
install -d -m 755 %{buildroot}%{_localstatedir}/log/%{pypi_name}

# Move config files to proper location
install -d -m 755 %{buildroot}%{_sysconfdir}/%{pypi_name}
mv %{buildroot}/usr/etc/%{pypi_name}/* %{buildroot}%{_sysconfdir}/%{pypi_name}
mv %{buildroot}/usr/etc/rootwrap.d %{buildroot}%{_sysconfdir}
install -p -D -m 640 etc/%{pypi_name}.conf %{buildroot}%{_sysconfdir}/%{pypi_name}/%{pypi_name}.conf

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-%{pypi_name}

# remove /usr/etc, it's not needed
# and the init.d script is in it, which is not needed
# because a systemd script is being included
rm -rf %{buildroot}/usr/etc/

# Install systemd units
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/openstack-%{pypi_name}-server.service
install -p -D -m 644 %{SOURCE3} %{buildroot}%{_unitdir}/openstack-%{pypi_name}-conductor.service

%check
#FIXME(ykarel) Enable once https://bugs.launchpad.net/tacker/+bug/1753645 is fixed.
#OS_TEST_PATH=./tacker/tests/unit ostestr --black-regex ipv6

%pre common
getent group %{pypi_name} >/dev/null || groupadd -r %{pypi_name}
getent passwd %{pypi_name} >/dev/null || \
    useradd -r -g %{pypi_name} -d %{_sharedstatedir}/%{pypi_name} -s /sbin/nologin \
    -c "OpenStack Tacker Daemons" %{pypi_name}
exit 0

%post
%systemd_post openstack-%{pypi_name}-server.service
%systemd_post openstack-%{pypi_name}-conductor.service

%preun
%systemd_preun openstack-%{pypi_name}-server.service
%systemd_preun openstack-%{pypi_name}-conductor.service

%postun
%systemd_postun_with_restart openstack-%{pypi_name}-server.service
%systemd_postun_with_restart openstack-%{pypi_name}-conductor.service

%files
%license LICENSE
%{_bindir}/%{pypi_name}*
%{_unitdir}/openstack-%{pypi_name}-server.service
%{_unitdir}/openstack-%{pypi_name}-conductor.service
%attr(-, root, %{pypi_name}) %{_sysconfdir}/%{pypi_name}/api-paste.ini

%files -n python%{pyver}-%{pypi_name}-tests
%license LICENSE
%{pyver_sitelib}/%{pypi_name}/tests

%files -n python%{pyver}-%{pypi_name}
%license LICENSE
%{pyver_sitelib}/%{pypi_name}
%{pyver_sitelib}/%{pypi_name}-*.egg-info
%exclude %{pyver_sitelib}/%{pypi_name}/tests

%files common
%license LICENSE
%doc README.rst
%dir %{_sysconfdir}/%{pypi_name}
%config(noreplace) %attr(0640, root, %{pypi_name}) %{_sysconfdir}/%{pypi_name}/%{pypi_name}.conf
%config(noreplace) %attr(0640, root, %{pypi_name}) %{_sysconfdir}/%{pypi_name}/policy.json
%config(noreplace) %attr(0640, root, %{pypi_name}) %{_sysconfdir}/%{pypi_name}/rootwrap.conf
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/rootwrap.d/%{pypi_name}.filters
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-%{pypi_name}
%dir %attr(0750, %{pypi_name}, root) %{_localstatedir}/log/%{pypi_name}
%dir %{_sharedstatedir}/%{pypi_name}
%dir %{_datadir}/%{pypi_name}

%if 0%{?with_doc}
%files -n python%{pyver}-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
