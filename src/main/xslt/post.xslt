<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<xsl:output method="html" indent="no" omit-xml-declaration="yes" standalone="no" encoding="UTF-8"/>

<xsl:template match="/post">
    <xsl:apply-templates/>
</xsl:template>

<xsl:template match="/post/body">
    <xsl:apply-templates/>
</xsl:template>

<xsl:template match="p|h1|h2|h3|h4|h5|h6">
    <xsl:element name="{local-name()}"><xsl:apply-templates/></xsl:element>
</xsl:template>

<xsl:template match="bible">
    <xsl:variable name=       "all_verses" select="count(./verse)"/>
    <xsl:variable name=  "numbered_verses" select="count(./verse[@i])"/>
    <xsl:variable name="unnumbered_verses" select="count(./verse[not(@i)])"/>

    <xsl:if test="($numbered_verses != 0) and ($unnumbered_verses != 0)">
      <xsl:message terminate="no">Bible quote contains a mix of numbered and not-numbered verses: <xsl:value-of select="."/></xsl:message>
    </xsl:if>

    <xsl:element name="div">
      <xsl:attribute name="class">skryba skryba-bible</xsl:attribute>
      <xsl:element name="div">
          <xsl:attribute name="class">skryba skryba-bible-address</xsl:attribute>
          <xsl:element name="span">
              <xsl:attribute name="class">skryba skryba-bible-address-book</xsl:attribute>
              <xsl:value-of select="./@book"/>
          </xsl:element>
          <xsl:element name="span">
              <xsl:attribute name="class">skryba skryba-bible-address-chapter</xsl:attribute>
              <xsl:value-of select="./@chapter"/>
          </xsl:element>
          <xsl:element name="span">
              <xsl:attribute name="class">skryba skryba-bible-address-verse</xsl:attribute>
              <xsl:value-of select="./@verse"/>
          </xsl:element>
          <xsl:element name="span">
              <xsl:attribute name="class">skryba skryba-bible-address-translation</xsl:attribute>
              <xsl:value-of select="./@translation"/>
          </xsl:element>
      </xsl:element>
      <xsl:element name="div">
          <xsl:attribute name="class">skryba skryba-bible-body</xsl:attribute>
          <xsl:apply-templates/>
      </xsl:element>
    </xsl:element>
</xsl:template>

<xsl:template match="verse">
    <xsl:element name="p">
        <xsl:attribute name="class">skryba skryba-bible-verse</xsl:attribute>
        <xsl:if test="@i">
            <xsl:element name="span">
                <xsl:attribute name="class">skryba skryba-bible-verse-number</xsl:attribute>
                <xsl:value-of select="@i"/>
            </xsl:element>
        </xsl:if>
        <xsl:apply-templates/>
    </xsl:element>
</xsl:template>

<xsl:template match="a">
  <xsl:variable name="h" select="./@href"/>
  <xsl:variable name="z" select="string-length($h)"/>

  <a>
    <xsl:attribute name="href">
      <xsl:choose>
        <!-- TODO use regex instead -->
        <!-- TODO add more protocols -->
        <xsl:when test="starts-with($h, 'http://') or starts-with($h, 'https://') or starts-with($h, 'ftp://')">
          <!-- absolute url, render as-is -->
          <xsl:value-of select="$h"/>
        </xsl:when>
        <xsl:when test="(4 &lt;= $z) and ('.xml' = substring($h, $z - 3))">
          <!-- cross-link to another post -->
          <xsl:value-of select="concat(substring($h, 1, $z - 3), 'html')"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:message terminate="no">WARNING: unknown link: <xsl:value-of select="$h"/></xsl:message>
          <xsl:value-of select="$h"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:attribute>
    <xsl:apply-templates/>
  </a>
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
