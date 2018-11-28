# ansible-cached-lookup

An Ansible lookup plugin that caches the results of any other lookup, most
useful in group/host vars.

By default, Ansible evaluates any lookups in a group/host var whenever the var
is accessed. For example, given a group/host var:

```yaml
content: "{{ lookup('pipe', 'a-very-slow-command' }}"
```

any tasks that access `content` (e.g. in a template) will re-evaluate the
lookup, which adds up very quickly. See
[ansible/ansible#9263](https://github.com/ansible/ansible/issues/9623).

## Installation

1. Pick a name that you want to use to call this plugin in Ansible playbooks.
   This documentation assumes you're using the name `cached`.

   ```
   pip install ansible-cached-lookup
   ```

2. Create a `lookup_plugins` directory in the directory in which you run Ansible.

   By default, Ansible will look for lookup plugins in an `lookup_plugins` folder
   adjacent to the running playbook. For more information on this, or to change
   the location where Ansible looks for lookup plugins, see the [Ansible
   docs](https://docs.ansible.com/ansible/dev_guide/developing_plugins.html#distributing-plugins).

3. Create a file called `cached.py` (or whatever name you picked) in the
   `lookup_plugins` directory, with one line:

   ```py
   from ansible_cached_lookup import LookupModule
   ```

## Contributing

To run the tests, run `tox`.

To format code to pass `tox -e lint`, run `tox -e format`.
