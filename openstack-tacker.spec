%global pypi_name tacker

%{!?upstream_version: %global upstream_version %{version}%{?milestone}}

Name:           openstack-%{pypi_name}
Version:        0.5.0
Release:        1%{?dist}
Summary:        OpenStack Tacker Service

License:        ASL 2.0
URL:            https://launchpad.net/%{pypi_name}
Source0:        http://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source1:        openstack-tacker-server.service
Source2:        tacker.logrotate

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-eventlet
BuildRequires:  python-heatclient
BuildRequires:  python-heat-translator
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

Requires: python-%{pypi_name} = %{version}-%{release}
Requires: python-%{pypi_name}-doc = %{version}-%{release}

Requires(pre): shadow-utils

%description
Support of Tacker for OpenStack.

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
Requires: python-neutronclient
Requires: python-novaclient
Requires: python-tosca-parser
Requires: python-heat-translator
Requires: python-crypto
Requires: python-paramiko

%description -n python-%{pypi_name}
OpenStack Tacker Service is an open policy framework for OpenStack

# Documentation package
%package -n python-%{pypi_name}-doc
Summary:        Documentation for OpenStack Tacker service

BuildRequires:  python-sphinx

%description -n python-%{pypi_name}-doc
Documentation for OpenStack Tacker service

%prep
%autosetup -n %{pypi_name}-%{upstream_version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

# Remove the requirements file so that pbr hooks don't add it
# to distutils requires_dist config
rm -rf {test-,}requirements.txt tools/{pip,test}-requires

%build
%py2_build

# Generate sample config and add the current directory to PYTHONPATH so
# oslo-config-generator doesn't skip tacker entry points.
PYTHONPATH=. oslo-config-generator --config-file=./etc/config-generator.conf --output-file=./etc/tacker.conf
#oslo-config-generator --config-file=./etc/config-generator.conf --output-file=./etc/tacker.conf

# generate html docs
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%py2_install


# Install config files
mv %{buildroot}%{_usr}%{_sysconfdir} %{buildroot}
install -p -D -m 640 etc/tacker.conf %{buildroot}%{_sysconfdir}/tacker/tacker.conf

# Install systemd script
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/openstack-tacker-server.service

# remove init script
rm -r %{buildroot}%{_sysconfdir}/init.d

# Install log file
install -d -m 755 %{buildroot}%{_localstatedir}/log/tacker

# Install logrotate
install -p -D -m 644 %{SOURCE2} %{buildroot}%{_sysconfdir}/logrotate.d/openstack-tacker


%pre
# Origin: http://fedoraproject.org/wiki/Packaging:UsersAndGroups#Dynamic_allocation
USERNAME=%{tacker_user}
GROUPNAME=%{tacker_group}
HOMEDIR=%{_sharedstatedir}/tacker
getent group $GROUPNAME >/dev/null || groupadd -r $GROUPNAME
getent passwd $USERNAME >/dev/null || \
  useradd -r -g $GROUPNAME -G $GROUPNAME -d $HOMEDIR -s /sbin/nologin \
  -c "Tacker Daemons" $USERNAME
exit 0

%post
%systemd_post openstack-tacker-server.service

%preun
%systemd_preun openstack-tacker-server.service

%postun
%systemd_postun_with_restart openstack-tacker-server.service

%files -n python-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/tacker*

%files
%{_bindir}/%{pypi_name}*
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/tacker/api-paste.ini
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/tacker/policy.json
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/tacker/tacker.conf
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/tacker/rootwrap.conf
%config(noreplace) %attr(0644, root, root) %{_sysconfdir}/rootwrap.d/tacker.filters
%{_unitdir}/openstack-tacker-server.service
%dir %attr(0755, tacker, tacker) %{_localstatedir}/log/tacker
%config(noreplace) %{_sysconfdir}/logrotate.d/openstack-tacker

%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html



%pre common


%changelog
* Mon Dec 19 2016 Dan Radez <dradez@redhat.com> - 0.5.0-1
- Initial Packaging
