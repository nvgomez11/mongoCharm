# Wordpress

## Description

Charm for Wordpress CMS

## Usage

`juju deploy mysql`

`juju deploy wordpress`

Add the relation

`juju add-relation wordpress mysql`


## Testing

The Python operator framework includes a very nice harness for testing
operator behaviour without full deployment. Just `run_tests`:

    ./run_tests
