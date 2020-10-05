%global milestone .0rc2
%global pypi_name tacker
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
OpenStack Tacker Service is an NFV Orchestrator for OpenStack

%global with_doc 1

Name:           openstack-%{pypi_name}
Version:        4.0.0
Release:        0.2%{?milestone}%{?dist}
Summary:        OpenStack Tacker Service

License:        ASL 2.0
URL:            https://launchpad.net/%{pypi_name}
Source0:        https://tarballs.opendev.org/openstack/%{pypi_name}/%{pypi_name}-%{upstream_version}.tar.gz
# patches_base=4.0.0.0rc2

Source1:        openstack-tacker-server.service
Source2:        tacker.logrotate
Source3:        openstack-tacker-conductor.service

BuildArch:      noarch

BuildRequires:  git
BuildRequires:  systemd
BuildRequires:  python3-castellan
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-eventlet
BuildRequires:  python3-heatclient
BuildRequires:  python3-heat-translator
BuildRequires:  python3-mistralclient
BuildRequires:  python3-neutronclient
BuildRequires:  python3-oslo-config
BuildRequires:  python3-oslo-log
BuildRequires:  python3-oslo-db
BuildRequires:  python3-oslo-policy
BuildRequires:  python3-oslo-service
BuildRequires:  python3-oslo-messaging
BuildRequires:  python3-oslo-versionedobjects
BuildRequires:  python3-paramiko
BuildRequires:  python3-routes
BuildRequires:  python3-tosca-parser
BuildRequires:  python3-webob
BuildRequires:  python3-barbicanclient
BuildRequires:  openstack-macros
BuildRequires:  python3-kubernetes
# Test dependencies
BuildRequires:  python3-cliff
BuildRequires:  python3-fixtures
BuildRequires:  python3-hacking
BuildRequires:  python3-mock
BuildRequires:  python3-oslotest
BuildRequires:  python3-glance-store
# For Fedora, the ostestr binary is provided by the %{__python3} subpackage
BuildRequires:  /usr/bin/ostestr
BuildRequires:  python3-sqlalchemy-filters
BuildRequires:  python3-subunit
BuildRequires:  python3-tackerclient
BuildRequires:  python3-tempest
BuildRequires:  python3-testrepository
BuildRequires:  python3-testtools

BuildRequires:  python3-webtest
BuildRequires:  python3-PyYAML

Requires: openstack-%{pypi_name}-common = %{version}-%{release}

Requires(pre): shadow-utils
%if 0%{?rhel} && 0%{?rhel} < 8
%{?systemd_requires}
%else
%{?systemd_ordering} # does not exist on EL7
%endif

%description
%{common_desc}

%package -n     python3-%{pypi_name}
Summary:        OpenStack Tacker Service
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires: python3-routes
Requires: python3-castellan
Requires: python3-eventlet
Requires: python3-glance-store >= 0.26.1
Requires: python3-requests
Requires: python3-keystonemiddleware >= 4.17.0
Requires: python3-kombu
Requires: python3-netaddr
Requires: python3-sqlalchemy
Requires: python3-sqlalchemy-filters
Requires: python3-webob
Requires: python3-heatclient >= 1.10.0
Requires: python3-keystoneclient >= 1:3.8.0
Requires: python3-alembic
Requires: python3-six
Requires: python3-stevedore
Requires: python3-oslo-concurrency >= 3.26.0
Requires: python3-oslo-config >= 2:5.2.0
Requires: python3-oslo-context >= 2.19.2
Requires: python3-oslo-db >= 5.0.0
Requires: python3-oslo-log >= 3.36.0
Requires: python3-oslo-messaging >= 9.3.0
Requires: python3-oslo-middleware >= 3.31.0
Requires: python3-oslo-policy >= 1.30.0
Requires: python3-oslo-reports >= 1.18.0
Requires: python3-oslo-rootwrap >= 5.8.0
Requires: python3-oslo-serialization >= 2.18.0
Requires: python3-oslo-service >= 1.24.0
Requires: python3-oslo-upgradecheck >= 0.1.0
Requires: python3-oslo-utils >= 3.33.0
Requires: python3-oslo-versionedobjects >= 1.33.3
Requires: python3-mistralclient >= 3.1.0
Requires: python3-neutronclient >= 6.7.0
Requires: python3-novaclient >= 1:9.1.0
Requires: python3-tosca-parser >= 1.6.0
Requires: python3-heat-translator >= 2.0.0
Requires: python3-cryptography
Requires: python3-paramiko
Requires: python3-pyroute2
Requires: python3-barbicanclient >= 4.5.2
Requires: python3-pbr
Requires: python3-kubernetes
Requires: python3-tooz
Requires: python3-jsonschema

Requires: python3-paste
Requires: python3-paste-deploy
Requires: python3-anyjson
Requires: python3-PyYAML
Requires: python3-openstacksdk >= 0.44.0
Requires: python3-rfc3986 >= 1.1.0

%description -n python3-%{pypi_name}
%{common_desc}

This package contains the Tacker python library.

%package common
Summary:  %{pypi_name} common files
Requires: python3-%{pypi_name} = %{version}-%{release}

%description common
%{common_desc}

This package contains the Tacker common files.

%package -n python3-%{pypi_name}-tests
Summary:    Tacker unit and functional tests
%{?python_provide:%python_provide python3-%{pypi_name}-tests}
Requires:   python3-%{pypi_name} = %{version}-%{release}

Requires:  python3-cliff
Requires:  python3-fixtures
Requires:  python3-mock
Requires:  python3-oslotest
Requires:  python3-os-testr
Requires:  python3-subunit
Requires:  python3-tackerclient
Requires:  python3-tempest
Requires:  python3-testrepository
Requires:  python3-testtools

Requires:  python3-webtest

%description -n python3-%{pypi_name}-tests
%{common_desc}

This package contains the Tacker unit and functional test files.

%if 0%{?with_doc}
%package -n python3-%{pypi_name}-doc
Summary:    Documentation for OpenStack Tacker service
%{?python_provide:%python_provide python3-%{pypi_name}-doc}

BuildRequires:  python3-sphinx
BuildRequires:  python3-openstackdocstheme
BuildRequires:  python3-sphinxcontrib-apidoc
BuildRequires:  python3-oslo-reports
BuildRequires:  python3-mistral

%description -n python3-%{pypi_name}-doc
Documentation for OpenStack Tacker service
%endif

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%{py3_build}

# Generate sample config and add the current directory to PYTHONPATH so
# oslo-config-generator doesn't skip tacker entry points.
PYTHONPATH=. oslo-config-generator --config-file=./etc/config-generator.conf --output-file=./etc/%{pypi_name}.conf

%if 0%{?with_doc}
# generate html docs
# (TODO) Remove -W option (warning-is-error) until https://review.openstack.org/#/c/557728 is
# merged.
sphinx-build -b html doc/source doc/build/html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo,htaccess} doc/build/html/_downloads
%endif

%install
%{py3_install}

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

%files -n python3-%{pypi_name}-tests
%license LICENSE
%{python3_sitelib}/%{pypi_name}/tests

%files -n python3-%{pypi_name}
%license LICENSE
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-*.egg-info
%exclude %{python3_sitelib}/%{pypi_name}/tests

%files common
%license LICENSE
%doc README.rst
%dir %{_sysconfdir}/%{pypi_name}
%config(noreplace) %attr(0640, root, %{pypi_name}) %{_sysconfdir}/%{pypi_name}/%{pypi_name}.conf
%config(noreplace) %attr(0640, root, %{pypi_name}) %{_sysconfdir}/%{pypi_name}/rootwrap.conf
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/rootwrap.d/%{pypi_name}.filters
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-%{pypi_name}
%dir %attr(0750, %{pypi_name}, root) %{_localstatedir}/log/%{pypi_name}
%dir %{_sharedstatedir}/%{pypi_name}
%dir %{_datadir}/%{pypi_name}

%if 0%{?with_doc}
%files -n python3-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html
%endif

%changelog
* Mon Oct 05 2020 RDO <dev@lists.rdoproject.org> 4.0.0-0.2.0rc1
- Update to 4.0.0.0rc2

* Tue Sep 29 2020 RDO <dev@lists.rdoproject.org> 4.0.0-0.1.0rc1
- Update to 4.0.0.0rc1

