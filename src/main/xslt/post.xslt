<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<xsl:include href="./util-date.xslt"/>
<xsl:include href="./util-tag.xslt"/>

<xsl:output method="html" indent="no" omit-xml-declaration="yes" standalone="no" encoding="UTF-8"/>

<xsl:template match="/post">
    <xsl:variable name="date" select="./@orig-date"/>
    <xsl:variable name="lang" select="./@lang"/>

    <!-- check if lang is valid -->
    <xsl:choose>
        <xsl:when test="$lang">
            <xsl:if test="not (('en' = $lang) or ('pl' = $lang))">
                <xsl:message terminate="no">invalid lang attribute: <xsl:value-of select="$lang"/></xsl:message>
            </xsl:if>
        </xsl:when>
        <xsl:otherwise>
            <xsl:message terminate="no">lang attribute missing!</xsl:message>
        </xsl:otherwise>
    </xsl:choose>

    <div class="skryba-post">
    <h1><xsl:value-of select="./title/text()"/></h1>

    <p class="skryba-post-date"><xsl:call-template name="renderDate">
        <xsl:with-param name="date"        select="./@orig-date"/>
        <xsl:with-param name="lang"        select="$lang"/>
    </xsl:call-template></p>

    <xsl:call-template name="renderTags">
        <xsl:with-param name="tags" select="./tags/text()"/>
    </xsl:call-template>

    <xsl:apply-templates/>
    </div>
</xsl:template>

<xsl:template match="/post/body">
    <div class="skryba-post-body"><xsl:apply-templates/></div>
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
