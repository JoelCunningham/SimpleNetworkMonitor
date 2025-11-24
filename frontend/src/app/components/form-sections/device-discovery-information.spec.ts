import { DeviceDiscoveryInformation } from '#components/form-sections';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('DeviceDiscoveryInformation', () => {
  let component: DeviceDiscoveryInformation;
  let fixture: ComponentFixture<DeviceDiscoveryInformation>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DeviceDiscoveryInformation],
    }).compileComponents();

    fixture = TestBed.createComponent(DeviceDiscoveryInformation);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
