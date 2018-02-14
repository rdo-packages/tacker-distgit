%global pypi_name tacker
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

%global common_desc \
OpenStack Tacker Service is an NFV Orchestrator for OpenStack

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
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-eventlet
BuildRequires:  python2-heatclient
BuildRequires:  python2-heat-translator
BuildRequires:  python2-mistralclient
BuildRequires:  python2-neutronclient
BuildRequires:  python2-oslo-config
BuildRequires:  python2-oslo-log
BuildRequires:  python2-oslo-db
BuildRequires:  python2-oslo-policy
BuildRequires:  python2-oslo-service
BuildRequires:  python2-oslo-messaging
BuildRequires:  python2-paramiko
BuildRequires:  python2-routes
BuildRequires:  python2-tosca-parser
BuildRequires:  python-webob
BuildRequires:  python2-barbicanclient
BuildRequires:  openstack-macros
BuildRequires:  python2-kubernetes
BuildRequires:  PyYAML
# Test dependencies
BuildRequires:  python2-cliff
BuildRequires:  python2-fixtures
BuildRequires:  python2-hacking
BuildRequires:  python2-mock
BuildRequires:  python2-oslotest
# For Fedora, the ostestr binary is provided by the python3 subpackage
BuildRequires:  /usr/bin/ostestr
BuildRequires:  python2-subunit
BuildRequires:  python2-tackerclient
BuildRequires:  python2-tempest
BuildRequires:  python2-testrepository
BuildRequires:  python2-testtools
BuildRequires:  python-webtest

Requires: openstack-%{pypi_name}-common = %{version}-%{release}

Requires(pre): shadow-utils
%{?systemd_requires}

%description
%{common_desc}

%package -n     python-%{pypi_name}
Summary:        OpenStack Tacker Service
%{?python_provide:%python_provide python2-%{pypi_name}}

Requires: python-paste
Requires: python-paste-deploy
Requires: python-routes
Requires: python-anyjson
Requires: python2-babel
Requires: python2-eventlet
Requires: python2-requests
Requires: python2-keystonemiddleware >= 4.17.0
Requires: python2-kombu
Requires: python2-netaddr
Requires: python2-sqlalchemy
Requires: python-webob
Requires: python2-heatclient >= 1.10.0
Requires: python2-keystoneclient >= 1:3.8.0
Requires: python2-alembic
Requires: python2-six
Requires: python2-stevedore
Requires: python2-oslo-concurrency >= 3.25.0
Requires: python2-oslo-config >= 2:5.1.0
Requires: python2-oslo-context >= 2.19.2
Requires: python2-oslo-db >= 4.27.0
Requires: python2-oslo-log >= 3.36.0
Requires: python2-oslo-messaging >= 5.29.0
Requires: python2-oslo-middleware >= 3.31.0
Requires: python2-oslo-policy >= 1.30.0
Requires: python2-oslo-reports >= 1.18.0
Requires: python2-oslo-rootwrap >= 5.8.0
Requires: python2-oslo-serialization >= 2.18.0
Requires: python2-oslo-service >= 1.24.0
Requires: python2-oslo-utils >= 3.33.0
Requires: python2-mistralclient >= 3.1.0
Requires: python2-neutronclient >= 6.3.0
Requires: python2-novaclient >= 9.1.0
Requires: python2-tosca-parser >= 0.8.1
Requires: python2-heat-translator  >= 0.4.0
Requires: python2-cryptography
Requires: python2-paramiko
Requires: python2-pyroute2
Requires: python2-barbicanclient >= 4.0.0
Requires: python2-pbr
Requires: python2-kubernetes
Requires: PyYAML

%description -n python-%{pypi_name}
%{common_desc}

This package contains the Tacker python library.

%package common
Summary:  %{pypi_name} common files
Requires: python-%{pypi_name} = %{version}-%{release}

%description common
%{common_desc}

This package contains the Tacker common files.

%package -n python-%{pypi_name}-tests
Summary:    Tacker unit and functional tests
Requires:   python-%{pypi_name} = %{version}-%{release}

Requires:  python2-cliff
Requires:  python2-fixtures
Requires:  python2-mock
Requires:  python2-oslotest
Requires:  python2-os-testr
Requires:  python2-subunit
Requires:  python2-tackerclient
Requires:  python2-tempest
Requires:  python2-testrepository
Requires:  python2-testtools
Requires:  python-webtest

%description -n python-%{pypi_name}-tests
%{common_desc}

This package contains the Tacker unit and functional test files.

%package -n python-%{pypi_name}-doc
Summary:    Documentation for OpenStack Tacker service

BuildRequires:  python2-sphinx
BuildRequires:  python2-openstackdocstheme
BuildRequires:  python2-oslo-reports
BuildRequires:  python-mistral

%description -n python-%{pypi_name}-doc
Documentation for OpenStack Tacker service

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
%py_req_cleanup

%build
%py2_build

# Generate sample config and add the current directory to PYTHONPATH so
# oslo-config-generator doesn't skip tacker entry points.
PYTHONPATH=. oslo-config-generator --config-file=./etc/config-generator.conf --output-file=./etc/%{pypi_name}.conf

# generate html docs
%{__python2} setup.py build_sphinx -b html
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%py2_install

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
OS_TEST_PATH=./tacker/tests/unit ostestr --black-regex ipv6

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

%files -n python-%{pypi_name}-tests
%license LICENSE
%{python2_sitelib}/%{pypi_name}/tests

%files -n python-%{pypi_name}
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-*.egg-info
%exclude %{python2_sitelib}/%{pypi_name}/tests

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

%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html

%changelog
