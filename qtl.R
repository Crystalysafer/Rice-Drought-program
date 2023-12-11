sug <- read.cross("csvs", ".", "gen.csv", "phe.csv",
                  genotypes = c("A", "H", "B"), map.function = "kosambi", crosstype = "riself")

summary_out <- data.frame()

sug <- calc.genoprob(sug, step = 1, map.function = "kosambi")


for (PheId in phenames(sug)[-1]) {

  out.em <- cim(cross = sug, pheno.col = PheId, method = "hk")
  out.em.sum <- summary(out.em, threshold = 2.5)
  
  if (dim(out.em.sum)[1] < 1)
    next
  
  mqtl <- makeqtl(sug, chr = out.em.sum[, 1], pos = out.em.sum[, 2], what = "prob")
  fqtl <- fitqtl(sug, dropone = T, get.ests = T, qtl = mqtl, method = "hk", pheno.col = PheId)
  qtl_eff <- round(summary(fqtl)[[length(fqtl)-1]][-1, 1], 2)
  qtl_pve <- round(summary(fqtl)[[length(fqtl)-2]][, 4], 2)
  
  for(tpm_i in 1:nrow(out.em.sum)){
    tpm <- lodint(out.em, chr = mqtl$chr[tpm_i], expandtomarkers=TRUE)
    tpm <- data.frame(TraitID=PheId, QTL=rownames(tpm)[2], Chr=tpm$chr[2], Pos=tpm$pos[2], 
                      LOD=tpm$lod[2], Add=qtl_eff[tpm_i], PVE=qtl_pve[tpm_i], 
                      LeftMarker=rownames(tpm)[1], LeftPos=tpm$pos[1], 
                      RightMarker=rownames(tpm)[3], RigthPos=tpm$pos[3])
    rbind(summary_out, tpm) -> summary_out
    
  }
  
  
}

write.csv(summary_out, file = "qtl_result.csv", row.names = FALSE)

