<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<!-- Renders out a date given in format: YYYY-MM-DD. -->
<xsl:template name="renderDateSimple">
    <!-- TODO better format check; XSLT 2.0 has support for regular expressions ... (fn:matches) -->
    <xsl:param name="date"/>
    <xsl:variable name="errorMsg">ERROR: invalid date format (<xsl:value-of select="$date"/>)</xsl:variable>

    <xsl:choose>
        <xsl:when test="10 = string-length($date)">
            <xsl:variable name="year"  select="number(substring($date, 1, 4))"/>
            <xsl:variable name="month" select="number(substring($date, 6, 2))"/>
            <xsl:variable name="day"   select="number(substring($date, 9, 2))"/>

            <xsl:variable name="month_pl">
                <xsl:choose>
                    <xsl:when test=" 1 = $month">stycznia</xsl:when>
                    <xsl:when test=" 2 = $month">lutego</xsl:when>
                    <xsl:when test=" 3 = $month">marca</xsl:when>
                    <xsl:when test=" 4 = $month">kwietnia</xsl:when>
                    <xsl:when test=" 5 = $month">maja</xsl:when>
                    <xsl:when test=" 6 = $month">czerwca</xsl:when>
                    <xsl:when test=" 7 = $month">lipca</xsl:when>
                    <xsl:when test=" 8 = $month">sierpnia</xsl:when>
                    <xsl:when test=" 9 = $month">września</xsl:when>
                    <xsl:when test="10 = $month">października</xsl:when>
                    <xsl:when test="11 = $month">listopada</xsl:when>
                    <xsl:when test="12 = $month">grudnia</xsl:when>
                    <xsl:otherwise>
                        <xsl:message terminate="yes"><xsl:value-of select="$errorMsg"/> (invalid month)</xsl:message>
                    </xsl:otherwise>
                </xsl:choose>
            </xsl:variable>

            <xsl:value-of select="concat($day, ' ', $month_pl, ', anno Domini nostri Jesu Christi ', $year)"/>
        </xsl:when>
        <xsl:otherwise>
            <xsl:message terminate="yes"><xsl:value-of select="$errorMsg"/></xsl:message>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<!-- Renders out a date given in format:

     YYYY-MM-DD

     or:

     YYYY-MM-DD; comment
.
-->
<xsl:template name="renderDate">
    <!-- TODO better format check; XSLT 2.0 has support for regular expressions ... (fn:matches) -->
    <xsl:param name="date" />
    <xsl:call-template name="renderDateSimple">
        <xsl:with-param name="date" select="substring($date, 1, 10)"/>
    </xsl:call-template>

    <xsl:if test="11 &lt;= string-length($date) and ';' = substring($date, 11, 1)">
        <xsl:value-of select="substring($date, 11)" disable-output-escaping="no"/>
    </xsl:if>
</xsl:template>

</xsl:stylesheet>
