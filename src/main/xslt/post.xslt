<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<!-- language: en (default), pl -->
<xsl:param name="lang"        select="'en'"/>
<xsl:param name="anno_domini" select="true()"/>

<xsl:include href="./util-date.xslt"/>
<xsl:include href="./util-tag.xslt"/>

<xsl:output method="html" indent="no" omit-xml-declaration="yes" standalone="no" encoding="UTF-8"/>

<xsl:template match="/post">
    <div id="post">
    <h1><xsl:value-of select="./title/text()"/></h1>

    <xsl:variable name="created_str">
        <xsl:choose>
            <xsl:when test="'pl' = $lang">Utworzono: </xsl:when>
            <xsl:otherwise>Created: </xsl:otherwise>
        </xsl:choose>
    </xsl:variable>

    <p id="post-date"><xsl:value-of select="$created_str"/><xsl:call-template name="renderDate">
        <xsl:with-param name="date"        select="./@orig-date"/>
        <xsl:with-param name="lang"        select="$lang"/>
        <xsl:with-param name="anno_domini" select="$anno_domini"/>
    </xsl:call-template></p>

    <xsl:call-template name="renderTags">
        <xsl:with-param name="tags" select="./tags/text()"/>
    </xsl:call-template>

    <xsl:apply-templates/>
    </div>
</xsl:template>

<xsl:template match="/post/body">
    <div id="post-body"><xsl:apply-templates/></div>
</xsl:template>

<xsl:template match="p">
    <p><xsl:apply-templates/></p>
</xsl:template>

<!-- void template -->
<xsl:template match="tags|title"/>

<!-- catch-all template -->
<xsl:template match="*">
    <xsl:message terminate="no">WARNING: Unmatched element: <xsl:value-of select="name()"/></xsl:message>
    <xsl:apply-templates/>
</xsl:template>

</xsl:stylesheet>
