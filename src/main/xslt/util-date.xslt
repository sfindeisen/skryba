<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">

<!-- Renders a date given in format: YYYY-MM-DD, where 1 <= MM <= 12.
     Use lang parameter to set the language: en (default), pl.
  -->
<xsl:template name="renderDateSimple">
    <!-- TODO better format check; XSLT 2.0 has support for regular expressions ... (fn:matches) -->
    <xsl:param name="date"/>
    <xsl:param name="lang"        select="'en'"/>

    <xsl:variable name="errorMsg">ERROR: invalid date format (<xsl:value-of select="$date"/>)</xsl:variable>

    <xsl:choose>
        <xsl:when test="10 = string-length($date)">
            <xsl:variable name="year"  select="number(substring($date, 1, 4))"/>
            <xsl:variable name="month" select="number(substring($date, 6, 2))"/>
            <xsl:variable name="day"   select="number(substring($date, 9, 2))"/>

            <xsl:if test="($month &lt; 1) or ($month &gt; 12)">
                <xsl:message terminate="yes"><xsl:value-of select="$errorMsg"/> (invalid month)</xsl:message>
            </xsl:if>
            <xsl:if test="($day &lt; 1) or ($day &gt; 31)">
                <xsl:message terminate="yes"><xsl:value-of select="$errorMsg"/> (invalid day)</xsl:message>
            </xsl:if>

            <xsl:variable name="month_str">
                <xsl:choose>
                    <xsl:when test="'en' = $lang">
                        <xsl:choose>
                            <xsl:when test=" 1 = $month">Jan</xsl:when>
                            <xsl:when test=" 2 = $month">Feb</xsl:when>
                            <xsl:when test=" 3 = $month">Mar</xsl:when>
                            <xsl:when test=" 4 = $month">Apr</xsl:when>
                            <xsl:when test=" 5 = $month">May</xsl:when>
                            <xsl:when test=" 6 = $month">Jun</xsl:when>
                            <xsl:when test=" 7 = $month">Jul</xsl:when>
                            <xsl:when test=" 8 = $month">Aug</xsl:when>
                            <xsl:when test=" 9 = $month">Sep</xsl:when>
                            <xsl:when test="10 = $month">Oct</xsl:when>
                            <xsl:when test="11 = $month">Nov</xsl:when>
                            <xsl:when test="12 = $month">Dec</xsl:when>
                        </xsl:choose>
                    </xsl:when>
                    <xsl:when test="'pl' = $lang">
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
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise><xsl:value-of select="$month"/></xsl:otherwise>
                </xsl:choose>
            </xsl:variable>

            <xsl:variable name="day_suffix">
                <xsl:choose>
                    <xsl:when test="'en' = $lang">
                        <xsl:choose>
                            <xsl:when test="(1 = $day) or (21 = $day) or (31 = $day)">st</xsl:when>
                            <xsl:when test="(2 = $day) or (22 = $day)">nd</xsl:when>
                            <xsl:when test="(3 = $day) or (23 = $day)">rd</xsl:when>
                            <xsl:otherwise>th</xsl:otherwise>
                        </xsl:choose>
                    </xsl:when>
                    <xsl:otherwise></xsl:otherwise>
                </xsl:choose>
            </xsl:variable>

            <xsl:variable name="day_str" select="concat($day, $day_suffix)"/>

            <span class="skryba-date-simple">
                <xsl:choose>
                    <xsl:when test="'en' = $lang">
                        <xsl:value-of select="concat($month_str, ' ', $day_str)"/>
                        <span class="skryba-date-year"><xsl:value-of select="$year"/></span>
                    </xsl:when>
                    <xsl:when test="'pl' = $lang">
                        <xsl:value-of select="concat($day_str, ' ', $month_str)"/>
                        <span class="skryba-date-year"><xsl:value-of select="$year"/></span>
                    </xsl:when>
                    <xsl:otherwise>
                        <xsl:value-of select="$date"/>
                    </xsl:otherwise>
                </xsl:choose>
            </span>
        </xsl:when>
        <xsl:otherwise>
            <xsl:message terminate="yes"><xsl:value-of select="$errorMsg"/></xsl:message>
        </xsl:otherwise>
    </xsl:choose>
</xsl:template>

<!-- Renders a date given in format:

     YYYY-MM-DD

     or:

     YYYY-MM-DD; comment

     where in each case 1 <= MM <= 12.

     Use lang parameter to set the language: en (default), pl.
  -->
<xsl:template name="renderDate">
    <!-- TODO better format check; XSLT 2.0 has support for regular expressions ... (fn:matches) -->
    <xsl:param name="date" />
    <xsl:param name="lang"        select="'en'"/>

    <span class="skryba-date"><xsl:call-template name="renderDateSimple">
        <xsl:with-param name="date"        select="substring($date, 1, 10)"/>
        <xsl:with-param name="lang"        select="$lang"/>
    </xsl:call-template>
    <xsl:if test="11 &lt;= string-length($date) and ';' = substring($date, 11, 1)">
        <span class="skryba-date-comment"><xsl:value-of select="substring($date, 12)" disable-output-escaping="no"/></span>
    </xsl:if>
    </span>
</xsl:template>

</xsl:stylesheet>
