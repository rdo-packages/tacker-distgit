%global pypi_name tacker
%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-%{pypi_name}
Version:        XXX
Release:        XXX
Summary:        OpenStack Tacker Service

License:        ASL 2.0
URL:            https://launchpad.net/%{pypi_name}
Source1:        tacker.logrotate
Source2:        openstack-tacker-server.service

BuildArch:      noarch

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
BuildRequires:  python-oslo-sphinx
BuildRequires:  python-paramiko
BuildRequires:  python-routes
BuildRequires:  python-tosca-parser
BuildRequires:  python-webob

Requires: python-%{pypi_name}-common = %{version}-%{release}

Requires(pre): shadow-utils

%description
OpenStack Tacker Service is an NFV Orchestrator for OpenStack

%package -n     python-%{pypi_name}
Summary:        OpenStack Tacker Service
%{?python_provide:%python_provide python2-%{pypi_name}}

Requires: python-tosca-parser
Requires: python-paste
Requires: python-paste-deploy
Requires: python-routes
Requires: python-anyjson
Requires: python-babel
Requires: python-eventlet
Requires: python-requests
Requires: python-keystonemiddleware
Requires: python-kombu
Requires: python-netaddr
Requires: python-sqlalchemy
Requires: python-webob
Requires: python-heatclient
Requires: python-keystoneclient
Requires: python-alembic
Requires: python-six
Requires: python-stevedore
Requires: python-oslo-concurrency
Requires: python-oslo-config
Requires: python-oslo-context
Requires: python-oslo-db
Requires: python-oslo-log
Requires: python-oslo-messaging
Requires: python-oslo-middleware
Requires: python-oslo-policy
Requires: python-oslo-reports
Requires: python-oslo-rootwrap
Requires: python-oslo-serialization
Requires: python-oslo-service
Requires: python-oslo-utils
Requires: python-oslo-sphinx
Requires: python-mistralclient
Requires: python-neutronclient
Requires: python-novaclient
Requires: python-tosca-parser
Requires: python-heat-translator
Requires: python-crypto
Requires: python-paramiko

%description -n python-%{pypi_name}
OpenStack Tacker Service is an NFV Orchestrator for OpenStack.

This package contains the Tacker python library.

%package common
Summary:  %{pypi_name} common files
Requires: python-%{pypi_name} = %{version}-%{release}

%description common
OpenStack Tacker Service is an NFV Orchestrator for OpenStack.

This package contains the Tacker common files.

%package -n python-%{pypi_name}-tests-unit
Summary:    Tacker unit tests
Requires:   python-%{pypi_name} = %{version}-%{release}

%description -n python-%{pypi_name}-tests-unit
OpenStack Tacker Service is an NFV Orchestrator for OpenStack.

This package contains the Tacker unit test files.

%package -n python-%{pypi_name}-doc
Summary:    Documentation for OpenStack Tacker service

BuildRequires:  python-sphinx

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
%{__python2} setup.py build_sphinx
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
mv %{buildroot}%{_sysconfdir}/%{pypi_name}/api-paste.ini %{buildroot}%{_sysconfdir}/%{pypi_name}/api-paste.ini

# Install logrotate
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-%{pypi_name}

# Install systemd units
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_unitdir}/openstack-%{pypi_name}-server.service

# remove init script
rm -r %{buildroot}%{_sysconfdir}/init.d

%pre common
getent group %{pypi_name} >/dev/null || groupadd -r %{pypi_name}
getent passwd %{pypi_name} >/dev/null || \
    useradd -r -g %{pypi_name} -d %{_sharedstatedir}/%{pypi_name} -s /sbin/nologin \
    -c "OpenStack Tacker Daemons" %{pypi_name}
exit 0

%post
%systemd_post openstack-%{pypi_name}-server.service

%preun
%systemd_preun openstack-%{pypi_name}-server.service

%postun
%systemd_postun_with_restart openstack-%{pypi_name}-server.service

%files
%license LICENSE
%{_bindir}/%{pypi_name}*
%{_unitdir}/openstack-%{pypi_name}-server.service
%attr(-, root, %{service}) %{_sysconfdir}/%{pypi_name}/api-paste.ini

%files -n python-%{pypi_name}-tests-unit
%license LICENSE
%{python2_sitelib}/%{service}/tests/unit

%files -n python-%{pypi_name}
%license LICENSE
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-*.egg-info
%exclude %{python2_sitelib}/%{pypi_name}/tests

%files common
%license LICENSE
$doc README.rst
%dir %{_sysconfdir}/%{pypi_name}
%config(noreplace) %attr(0640, root, %{pypi_name}) %{_sysconfdir}/%{pypi_name}/%{pypi_name}.conf
%config(noreplace) %attr(0640, root, %{pypi_name}) %{_sysconfdir}/%{pypi_name}/policy.json
%config(noreplace) %attr(0640, root, %{pypi_name}) %{_sysconfdir}/%{pypi_name}/rootwrap.conf
%dir %{_sysconfdir}/%{pypi_name}/rootwrap.d
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/%{pypi_name}/rootwrap.d/%{pypi_name}.filters
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-%{pypi_name}
%dir %attr(0750, %{pypi_name}, root) %{_localstatedir}/log/%{pypi_name}
%dir %{_sharedstatedir}/%{pypi_name}
%dir %{_datadir}/%{pypi_name}

%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html

%changelog
