# KNX Project to Home Assistant config converter

Utility tool to convert a KNX project into a Home Assistant configuration. It
depends on [xknxproject] for parsing of the actual ETS project.

## Concept

The configuration in ETS can be placed in the "comment" section for a group address.

~~~
```hassos
<entity_type>:
  <params>
```
~~~

### Light

To connect a [ha-knx-light](Light) device type with a group address use the
following comment:

~~~
```hassos
light:
  name: <name>
```
~~~

The `address` and `state_address` parameter are automatically set to be the GA
address to which the comment belongs too.

[xknxproject]: https://github.com/XKNX/xknxproject
[ha-knx-light]: https://www.home-assistant.io/integrations/knx/#light
