## [TR](#Valf) [EN](#Valf-|-EN)
# VALF
[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)]()

Valf, tamamen açık kaynaklı olarak, Sistem Yöneticileri düşünülerek tasarlanmış bir uzaktan yönetim aracıdır.

➤ Valf,

* Uzak sunucularınızı ve onların kayıtlı niteliklerini görebilmenizi,
* Yeni sunucular ekleyebilmenizi, var olanları silebilmenizi,
* Bağlantılara yeni nitelikler ekleyebilmenizi, silebilmenizi,
* Nitelikleri değiştirebilmenizi,
* Oluşturulmuş SSH sertifikalarınızı görebilmenizi,
* Herkese açık anahtarları arayüz üzerinden görüntüleyebilmenizi,
* Yeni sertifikalar ekleyebilmenizi, var olanları silebilmenizi,
* Sertifikalarınızı seçtiğiniz sunuculara göndermenizi,
* Tanımladığınız sertifikaları silebilmenizi,
* Arayüz üzerinde açılan bir terminal ile tek tıkla SSH bağlantısı kurabilmenizi,
* SCP protokolünü kullanarak yerel bilgisayarınızdaki dosyalarınızı uzak sunucularınızın /home/user dizinine gönderebilmenizi,
* SFTP protokolünü kullanarak dinamik olarak hem yerel hem de uzak sunucularınızın dosya dizinlerinde gezinebilmenizi,
* Görsel arayüz içerisinde **'Sürükle-Bırak'** ile yerel dosyalarınızı/dizinlerinizi uzak sunucularınıza gönderebilmenizi sağlar.

➤ Ayrıca SSH sertifikalarınızı uzak sunucularınıza tanımlanamanız veya halihazırda tanımlamış olmanız sayesinde Valf sizden,

* SSH bağlantısı kurarken,
* SFTP protokolü ile dosya aktarırken parola girmenizi beklemez.

## Fonksiyonlar
[![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/colored.png)]()

Valf yapısı ve amacı gereği birden fazla alanda Sistem Yöneticilerine kolaylık sağladığından birden fazla alanda ayrı fonksiyonlara sahiptir. 

**Bu fonksiyonlardan hiçbiri bilgilerinizi yerel makinenize veya uzak sunuculara kaydetmez/depolamaz. Valf kapandığında değişkenlerde tutulan tüm değerler bir daha görünmemek üzere silinir.**

## Bağlantı Fonksiyonları
![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)
* [Bağlantıları ve özelliklerini arayüzde görmek](#Bağlantıları-ve-Özelliklerini-Arayüzde-Görmek)
* [Yeni bağlantı eklemek](#Yeni-Bağlantı-Eklemek)
* [Bağlantı silmek](#Bağlantı-silmek)
* [Bağlantıya yeni nitelik eklemek](#Bağlantıya-Yeni-Nitelik-Eklemek)
* [Bağlantı niteliklerini silmek](#Bağlantı-niteliklerini-silmek)
* [Bağlantı niteliklerini düzenlemek](#Bağlantı-niteliklerini-düzenlemek)
## Sertifika Fonksiyonları
![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)
* [Sertifikaları ve açık anahtarlarını arayüzde görmek](#Sertifikaları-ve-açık-anahtarlarını-arayüzde-görmek)
* [Yeni sertifika eklemek](#Yeni-sertifika-eklemek)
* [Sertifika silmek](#Sertifika-Silmek)
* [Sertifikaları sunuculara tanımlamak](#Sertifikaları-sunuculara-tanımlamak)
* [Tanımlı sertifikaları silmek](#Tanımlı-sertifikaları-silmek)
## Bağlantı Kurma ve Dosya Aktarım Fonksiyonları
![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)
* [SSH bağlantısı kurmak](#SSH-bağlantısı-kurmak)
* [SCP ile dosya transferi yapmak](#SCP-ile-dosya-transferi-yapmak)
* [SFTP ile yerel makine/uzak sunucu dosya sistemlerinde gezmek](#SFTP-ile-yerel-makine/uzak-sunucu-dosya-sistemlerinde-gezmek)
* [SFTP ile dosya/dizin transferi yapmak](#SFTP-ile-dosya/dizin-transferi-yapmak)

## Ek Başlıklar
![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

* [Katkıda bulunmak isteyenler için](#Katkıda-bulunmak-isteyenler-için)
* [Test edilen dağıtımlar](#Test-edilen-dağıtımlar)
* [Lisans](#Lisans)

## Fonksiyonların Kullanımı ve Detaylı Açıklamaları
## Bağlantı Fonksiyonları
![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)
## Bağlantıları ve Özelliklerini Arayüzde Görmek
![](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/vintage.png)

Valf tüm yönleriyle kullanıcılarına sadelik ve kolaylık sunma amacı ile tasarlanmıştır. Bu sebepten ötürü temel amacımızın yapı taşı olan uzak sunucularınız sürekli olarak arayüzün sol tarafında sergilenir. Bu sunucuların üzerinde iki adet etkide bulunabilirsiniz. 

Sol tıkladığınızda arayüzün kalan kısmında sunucu özellikleriniz yer alır. **Burada herhangi bir kural yoktur. Önceden kaydettiğiniz sunucu nitelikleriniz istediği sırayla burada yer alabilir. Valf, satır aralarında boşluk veya satır sıralarının nizami olmasını gözetmez.**

Sağ tıkladığınızda ise sunucu üzerinde gerçekleştirebileceğiniz diğer etkilerden bir kaçı sizi karşılar. Bu özelliklerin tamamı çalıştırılabilir yapıdadır ve ileriki başlıklarda anlatılacaktır.

**Valf'i başlattığınızda eğer daha önce hiç SSH bağlantısı kurmamışsanız /home/user dizininizin altına /.ssh/ dizinini ve altında bulunması gereken authorized_keys, config, known_hosts dosyalarını oluşturur.**

## Yeni Bağlantı Eklemek
![](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/vintage.png)

Yeni bağlantı eklemek için sadece temel değerlere sahip olmanız yeterli. Valf, arayüze girdiğiniz bağlantınıza vereceğiniz ad, IP ve kullanıcı adı bilgilerini sizin yerinize sistemli bir şekilde .ssh/config dosyanıza kaydeder. Sonrasında da onlara tek tıkla ulaşmanızı sağlar.

## Bağlantı Silmek
![](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/vintage.png)

Artık kullanmadığınız sunucuların config dosyanızda yer kaplamasına gerek yok ! Ya da onları bulmak için gözlerinizi bozmanıza. Valf ile yalnızca sunucu adına sağ tıklayarak açtığınız pencereden Bağlantıyı Sil'i seçmeniz yeterli. O sizin için istediğiniz sunucuyu ve ona ait tüm özellikleri saliseler içerisinde dosyanızdan siler.

## Bağlantıya Yeni Nitelik Eklemek
![](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/vintage.png)

Sunucunuza yeni nitelikler eklemek hiç bu kadar kolay olmamıştı ! İstediğiniz değeri istediğiniz sunucunuza anında ekleyebilirsiniz. Valf sizin için config dosyanızda alakalı sunucunun en son satırına bu değeri kaydeder ve karşılığında sizden hiçbir şey beklemez. 

## Bağlantı Niteliklerini Silmek
![](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/vintage.png)

Yeni nitelikler eklemek kadar bu nitelikleri silmek de meziyet ister. Valf, artık kullanmadığınız ya da geçersiz hale gelen sunucu niteliklerinizi config dosyanızdan siler ve arkasında hiç iz bırakmaz.

## Bağlantı Niteliklerini Düzenlemek
![](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/vintage.png)

Sunucu IP'nizi yanlış mı yazdınız ? Durun, çaresizlikle terminali açıp bir rakam için bir ton işlem yapmanıza gerek yok. Valf ile arayüz üzerinde istediğiniz nitelikteki istediğiniz değeri değiştirin, değişiklikten sonra 'Niteliği Değiştir' butonuna tıklasanız yeterli. Gerisini Valf'e bırakın.

## Sertifika Fonksiyonları
![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

## Sertifikaları ve Açık Anahtarlarını Arayüzde Görmek
![](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/vintage.png)

Sertifikaların sunucu yönetiminde her gün dakikalarca zaman kazandırdığının farkında olarak Valf'e sertifikaları eklememek düşünülemezdi. Valf sayesinde her seferinde bir yerlere parola girmek zorunda değilsiniz. Sertifikalarım menüsündeki sertifikalarınızdan dilediğiniz bir tanesine sağ tıklayıp sunucuya gönder demeniz yeterli. 

Eğer sertifikaların içeriğini merak ediyorsanız sol tıklayarak onları da görüntüleyebilir ve kopyalayabilirsiniz. 

## Yeni Sertifika Eklemek
![](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/vintage.png)

Hiç sertifikanız olmayabilir, ya da her sunucuya ayrı sertifika göndermek istiyor olabilirsiniz. Valf açısından sorun yok. Yeni sertifika oluşturma özelliği sayesinde istediğiniz ad ve parolada yeni bir sertifika oluşturabilirsiniz. Eğer parola girmezseniz parolasız, ad girmezseniz default adında, her ikisini de girmezseniz hem default adda hem de parolasız bir sertifika oluşturabilirsiniz. Hangisini yapacağınızı seçmek tamamen size kalmış !

## Sertifika Silmek
![](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/vintage.png)

Kullanmadığınız ya da parolasının/gizli anahtarının ele geçirilmiş olabileceğinizi düşündüğünüz sertifikaları sadece sağ tıklayarak makinenizden silebilirsiniz. (Bu fonksiyon sadece ana makineden silme işlemi yapar.)

## Sertifikaları Sunuculara Tanımlamak
![](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/vintage.png)

İşte Valf'in sertifikalar konusundaki asıl olayı. Sertifikanız üzerine sağ tıklayın. Sertifikayı gönder'i seçin. İstediğiniz sunucuyu seçin, parolasını girin ve işte oldu ! Artık SSH ile parolasız bağlantı kurabilir ve SFTP ile parolasız sunucunuza bağlanıp istediğiniz kadar dosya/dizin aktarabilirsiniz !

## Tanımlı Sertifikaları Silmek
![](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/vintage.png)

Sunucularınıza gönderdiğiniz bir sertifikada güvenlik açığı oluşturabilecek bir durum yaşadınız veya artık o sunucuya erişmenize gerek yok. Durum her ne olursa olsun günün birinde uzak sunucularınızdan birinden sertifikanızı silmek isteyebilirsiniz. Tanımlı sertifika silmek istediğiniz sunucunuza sağ tıklayıp sertifikanızı silin ve sunucu ile olan ilişkinizi tek seferde kesip atın !

## Bağlantı Kurma ve Dosya Aktarım Fonksiyonları
![-----------------------------------------------------](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/aqua.png)

Bu başlık altında listelenen fonksiyonlar hem SSH sertifikası tanımlanmış sunucular için hem de tanımlanmamış sunucular için iki farklı durum da göz önünde bulundurularak açıklanacaktır.

## SSH Bağlantısı Kurmak
![](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/vintage.png)

* Eğer SSH sertifikası tanımlanmışsanız, işiniz herkesten kolay. Bağlanmak istediğiniz sunucuya sağ tıklayın, Bağlan'ı seçin. Arayüz üzerinden sunucu yönetimi yapmanın ne kadar keyifli olduğunu farkedin ve bunun tadını çıkarın.

* Eğer SSH sertifikası tanımlamamışsanız (ki tanımlamanın dünyayı daha güzel bir yer haline getireceği kesindir), bağlanmak istediğiniz sunucuya sağ tıklayın, Bağlan'ı seçin, parolanızı girin ve Valf'in tadını çıkarın.

## SCP ile Dosya Transferi Yapmak
![](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/vintage.png)
**Not : Valf henüz bu fonksiyon için SSH sertifikanız olup olmadığını kontrol etmiyor. Eğer buna bir dur demek isterseniz pull request taleplerine her zaman açığız.**

SCP ile SFTP yeni sunucular açtığınızda en büyük destekçileriniz, bunun farkındayız. Tabii Valf de öyle. Eğer dosyalarınızı SCP vasıtası ile aktarmak isterseniz sunucunuza sağ tıklayıp Scp ile dosya aktar'ı seçin. Parolanızı girin ve sürekli açık olacak Dosya Seç butonuna tıklayıp göndermek istediğiniz dosyayı seçin. Seçtiğiniz dosya saniyeler içerisinde uzak sunucunuzun /home/user dizininde belirecek !

## SFTP ile Yerel Makine/Uzak Sunucu Dosya Sistemlerinde Gezmek
![](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/vintage.png)

**Not: Burada her arama sayfadaki fonksiyonları tekrar çağırarak sıfırlanmasına sebep olmaktadır. Eğer buna bir dur demek isterseniz pull request taleplerine açığız.**

* Eğer SSH sertifikası tanımlamışsanız, sunucunuza sol tıklayıp, sağ tarafta yer alan SFTP ile bağlan butonuna basın. Karşınızda iki sunucunun da /home/user dizinlerinden başlayan dosya sistemlerini bulacaksınız. Üstlerinde yer alan arama kısımları işte bu başlığın olayı. Eğer daha üst veya alt dizinleri ağaç yapısında aramadan direk geçiş yapmak istiyorsanız buraya istediğiniz dizini yazın. Dizinleme işlemi verdiğiniz noktadan başlayacaktır. 

* Eğer SSH sertifikası tanımlamamışsanız, sunucunuza sol tıklayıp, sağ tarafta yer alan SFTP ile bağlan butonuna basın, gelen parola penceresine parolanızı girin. Karşınızda iki sunucunun da /home/user dizinlerinden başlayan dosya sistemlerini bulacaksınız. Üstlerinde yer alan arama kısımları işte bu başlığın olayı. Eğer daha üst veya alt dizinleri ağaç yapısında aramadan direk geçiş yapmak istiyorsanız buraya istediğiniz dizini yazın. Dizinleme işlemi verdiğiniz noktadan başlayacaktır. 

## SFTP ile Dosya/Dizin Transferi Yapmak
![](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/vintage.png)

Valf'in en önemli ve en kolaylık sağlayan özelliği, SFTP ile dosya veya dizin transferi yapmak. Bu büyülü özellik sayesinde artık sancılı dosya transferi yapma süreçlerine son verebilirsiniz. Çünkü Valf sizin için en kolay hale getiriyor.

* Eğer SSH sertifikası tanımlamışsanız, sunucunuza sol tıklayıp, sağ tarafta yer alan SFTP ile bağlan butonuna basın. Karşınızda iki sunucunun da /home/user dizinlerinden başlayan dosya sistemlerini bulacaksınız. Bu dosya ağaçları isterseniz yukarıdaki başlıkta anlatıldığı üzere istediğiniz noktadan başlatın, istediğiniz dosya/dizini karşı makinedeki istediğiniz yola **sürükleyip bırakın**. İşte bu kadar, siz ne olduğunu anlamadan gönderikleriniz çoktan karşı tarafta belirmiş olacak !

* Eğer SSH sertifikası tanımlamamışsanız, sunucunuza sol tıklayıp, sağ tarafta yer alan SFTP ile bağlan butonuna basın, gelen parola penceresine parolanızı girin. Karşınızda iki sunucunun da /home/user dizinlerinden başlayan dosya sistemlerini bulacaksınız. Bu dosya ağaçları isterseniz yukarıdaki başlıkta anlatıldığı üzere istediğiniz noktadan başlatın, istediğiniz dosya/dizini karşı makinedeki istediğiniz yola **sürükleyip bırakın**. İşte bu kadar, siz ne olduğunu anlamadan gönderikleriniz çoktan karşı tarafta belirmiş olacak !

# Katkıda Bulunmak İsteyenler İçin
![](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

README dosyası boyunca anlatılan özellikler içerisinde Valf'de olmasını istediğimiz ancak çeşitli faktörler sebebi ile eklenemeyen bazı özelliklere yer verilmiştir. Katkıda bulunmak isteyen Açık Kaynak Gönüllüleri Valf'e öncelikle bu noktalardan destek verebilirler.

# Test Edilen Dağıtımlar
![](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

* Pardus 19.03 XFCE
* Ubuntu 20.04

*Not: Burada yer almayan bir sürümde Valf'i sorunsuz kullanabiliyorsanız lütfen bize bildirin.*

# Lisans
![](https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/solar.png)

Bu depo MIT lisansı ile lisanslanmıştır.

# VALF | EN
