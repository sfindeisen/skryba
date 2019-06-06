<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<!-- tag string format: tag one; some-other; yet another ... ; -->
<xsl:template name="renderTagList">
    <xsl:param name="tags"/>

    <xsl:variable name="t" select="substring-before($tags, ';')"/>
    <xsl:variable name="u" select="normalize-space($t)"/>
    <xsl:variable name="z" select="string-length($t)"/>

    <!-- output the first tag -->
    <xsl:if test="$u">
        <li class="skryba-tag"><xsl:value-of select="$u" disable-output-escaping="no"/></li>
    </xsl:if>

    <!-- recursive call -->
    <xsl:if test="(2+$z) &lt;= string-length($tags)">
        <xsl:call-template name="renderTagList">
            <xsl:with-param name="tags" select="substring($tags, (2+$z))"/>
        </xsl:call-template>
    </xsl:if>
</xsl:template>

<xsl:template name="renderTags">
    <xsl:param name="tags"/>

    <ul class="skryba-tag-list"><xsl:call-template name="renderTagList">
        <xsl:with-param name="tags" select="concat($tags, ';')"/>
    </xsl:call-template></ul>
</xsl:template>

</xsl:stylesheet>
