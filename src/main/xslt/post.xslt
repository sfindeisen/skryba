<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<xsl:output method="html" indent="no" omit-xml-declaration="yes" standalone="no" encoding="UTF-8"/>

<xsl:template match="/post">
    <xsl:apply-templates/>
</xsl:template>

<xsl:template match="/post/body">
    <xsl:apply-templates/>
</xsl:template>

<xsl:template match="p">
    <p><xsl:apply-templates/></p>
</xsl:template>

<xsl:template match="img">
  <img>
    <xsl:attribute name="alt"><xsl:value-of select="./@alt"/></xsl:attribute>
    <xsl:attribute name="src">../<xsl:value-of select="./@src"/></xsl:attribute>
  </img>
</xsl:template>

<!-- void template -->
<xsl:template match="tags|title"/>

<!-- catch-all template -->
<xsl:template match="*">
    <xsl:message terminate="no">WARNING: Unmatched element: <xsl:value-of select="name()"/></xsl:message>
    <xsl:apply-templates/>
</xsl:template>

</xsl:stylesheet>
