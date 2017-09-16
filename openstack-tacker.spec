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
BuildRequires:  python-setuptools
BuildRequires:  python-eventlet
BuildRequires:  python-heatclient
BuildRequires:  python-heat-translator
BuildRequires:  python-mistralclient
BuildRequires:  python-neutronclient
BuildRequires:  python-oslo-config
BuildRequires:  python-oslo-log
BuildRequires:  python-oslo-db
BuildRequires:  python-oslo-policy
BuildRequires:  python-oslo-service
BuildRequires:  python-oslo-messaging
BuildRequires:  python-paramiko
BuildRequires:  python-routes
BuildRequires:  python-tosca-parser
BuildRequires:  python-webob
BuildRequires:  python-barbicanclient
# Test dependencies
BuildRequires:  python-cliff
BuildRequires:  python-fixtures
BuildRequires:  python-hacking
BuildRequires:  python-mock
BuildRequires:  python-oslotest
# For Fedora, the ostestr binary is provided by the python3 subpackage
BuildRequires:  /usr/bin/ostestr
BuildRequires:  python-subunit
BuildRequires:  python-tackerclient
BuildRequires:  python-tempest
BuildRequires:  python-testrepository
BuildRequires:  python-testtools
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
Requires: python-babel
Requires: python-eventlet
Requires: python-requests
Requires: python-keystonemiddleware >= 4.12.0
Requires: python-kombu
Requires: python-netaddr
Requires: python-sqlalchemy
Requires: python-webob
Requires: python-heatclient >= 1.6.1
Requires: python-keystoneclient >= 1:3.8.0
Requires: python-alembic
Requires: python-six
Requires: python-stevedore
Requires: python-oslo-concurrency >= 3.8.0
Requires: python-oslo-config >= 2:4.0.0
Requires: python-oslo-context >= 2.14.0
Requires: python-oslo-db >= 4.24.0
Requires: python-oslo-log >= 3.22.0
Requires: python-oslo-messaging >= 5.24.2
Requires: python-oslo-middleware >= 3.27.0
Requires: python-oslo-policy >= 1.23.0
Requires: python-oslo-reports >= 0.6.0
Requires: python-oslo-rootwrap >= 5.0.0
Requires: python-oslo-serialization >= 1.10.0
Requires: python-oslo-service >= 1.10.0
Requires: python-oslo-utils >= 3.20.0
Requires: python-mistralclient >= 3.1.0
Requires: python-neutronclient >= 6.3.0
Requires: python-novaclient >= 1:9.0.0
Requires: python-tosca-parser >= 0.8.1
Requires: python-heat-translator  >= 0.4.0
Requires: python-cryptography
Requires: python-paramiko
Requires: python-pyroute2
Requires: python-barbicanclient >= 4.0.0
Requires: python-pbr

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

Requires:  python-cliff
Requires:  python-fixtures
Requires:  python-mock
Requires:  python-oslotest
Requires:  python-os-testr
Requires:  python-subunit
Requires:  python-tackerclient
Requires:  python-tempest
Requires:  python-testrepository
Requires:  python-testtools
Requires:  python-webtest

%description -n python-%{pypi_name}-tests
%{common_desc}

This package contains the Tacker unit and functional test files.

%package -n python-%{pypi_name}-doc
Summary:    Documentation for OpenStack Tacker service

BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme
BuildRequires:  python-oslo-reports
BuildRequires:  python-mistral

%description -n python-%{pypi_name}-doc
Documentation for OpenStack Tacker service

%prep
%autosetup -n %{pypi_name}-%{upstream_version} -S git

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

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
