## -*- coding: utf-8; mode: html; -*-
<%inherit file="tailbone:templates/base_meta.mako" />

<%def name="favicon()">
  ## <link rel="icon" type="image/x-icon" href="${request.static_url('tailbone_theo.web:static/favicon.ico')}" />
  <link rel="icon" type="image/x-icon" href="${request.static_url('tailbone:static/img/rattail.ico')}" />
</%def>

<%def name="header_logo()">
  ${h.image(request.static_url('tailbone:static/img/rattail.ico'), "Header Logo", style="height: 49px;")}
</%def>

<%def name="footer()">
  <p class="has-text-centered">
    ${h.link_to("Theo {}{}".format(theo.__version__, '' if request.rattail_config.production() else '+dev'), url('about'))}
  </p>
</%def>
