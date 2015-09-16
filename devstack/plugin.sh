# plugin.sh - DevStack plugin.sh dispatch script ceilometer_infoblox

function install_ceilometer_infoblox {
    cd $CEILOMETER_INFOBLOX_DIR
    sudo python setup.py install
}

function init_ceilometer_infoblox {
    echo
}

function configure_ceilometer_infoblox {
    iniset $CEILOMETER_CONF infoblox snmp_community $CEILOMETER_INFOBLOX_SNMP_COMMUNITY
}

# check for service enabled
if is_service_enabled ceilometer-infoblox; then

    if [[ "$1" == "stack" && "$2" == "pre-install" ]]; then
        # Set up system services
        echo_summary "Configuring system services for Infoblox Ceilometer"
        #install_package cowsay

    elif [[ "$1" == "stack" && "$2" == "install" ]]; then
        # Perform installation of service source
        echo_summary "Installing Infoblox Ceilometer"
        install_ceilometer_infoblox

    elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
        # Configure after the other layer 1 and 2 services have been configured
        echo_summary "Configuring Infoblox ceilometer"
        configure_ceilometer_infoblox

    elif [[ "$1" == "stack" && "$2" == "extra" ]]; then
        # Initialize and start the ceilometer-infoblox service
        echo_summary "Initializing Infoblox Ceilometer"
        init_ceilometer_infoblox
    fi

    if [[ "$1" == "unstack" ]]; then
        # Shut down ceilometer_infoblox services
        # no-op
        :
    fi

    if [[ "$1" == "clean" ]]; then
        # Remove state and transient data
        # Remember clean.sh first calls unstack.sh
        # no-op
        :
    fi
fi
